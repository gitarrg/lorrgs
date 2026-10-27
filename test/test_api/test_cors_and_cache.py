"""CORS allow-list and cache headers stay safe for a shared CDN cache."""

import asyncio

import fastapi
import pytest
from fastapi.responses import JSONResponse

from lorrgs_api.middlewares import cache_middleware, cors_middleware


def _app() -> fastapi.FastAPI:
    app = fastapi.FastAPI()

    @app.get("/ok")
    def ok():
        return {"ok": True}

    @app.get("/short")
    def short(response: fastapi.Response):
        response.headers["Cache-Control"] = "max-age=300"
        return {"ok": True}

    @app.get("/fail")
    def fail():
        return JSONResponse({"detail": "no"}, status_code=500)

    cors_middleware.init(app)
    cache_middleware.init(app)
    return app


async def _request(path: str, origin: str | None = None) -> tuple[int, dict[str, str]]:
    status_code = 0
    raw_headers: list[tuple[bytes, bytes]] = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        nonlocal status_code, raw_headers
        if message["type"] == "http.response.start":
            status_code = message["status"]
            raw_headers = list(message.get("headers") or [])

    headers = []
    if origin is not None:
        headers.append((b"origin", origin.encode()))

    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "GET",
        "scheme": "https",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": headers,
        "client": ("127.0.0.1", 123),
        "server": ("test", 443),
    }
    await _app()(scope, receive, send)

    decoded: dict[str, str] = {}
    for key, value in raw_headers:
        name = key.decode().lower()
        text = value.decode()
        decoded[name] = f"{decoded[name]}, {text}" if name in decoded else text
    return status_code, decoded


def test_success_varies_on_origin_and_keeps_route_cache(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEBUG", raising=False)
    status, headers = asyncio.run(_request("/short", "https://lorrgs.io"))

    assert status == 200
    assert headers["cache-control"] == "max-age=300"
    assert headers["access-control-allow-origin"] == "https://lorrgs.io"
    assert "origin" in headers["vary"].lower()


def test_default_cache_and_vary_without_an_origin(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEBUG", raising=False)
    status, headers = asyncio.run(_request("/ok"))

    assert status == 200
    assert headers["cache-control"] == "max-age=3600"
    assert "access-control-allow-origin" not in headers
    assert "origin" in headers["vary"].lower()


def test_pages_preview_origin_is_allowed(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEBUG", raising=False)
    origin = "https://feature.lorrgs-frontend.pages.dev"
    _, headers = asyncio.run(_request("/ok", origin))

    assert headers["access-control-allow-origin"] == origin


def test_pages_project_host_is_allowed(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEBUG", raising=False)
    origin = "https://lorrgs-frontend.pages.dev"
    _, headers = asyncio.run(_request("/ok", origin))

    assert headers["access-control-allow-origin"] == origin


def test_forever_site_origin_is_allowed(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEBUG", raising=False)
    origin = "https://forever.lorrgs.io"
    _, headers = asyncio.run(_request("/ok", origin))

    assert headers["access-control-allow-origin"] == origin


def test_unknown_origin_is_rejected(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEBUG", raising=False)
    _, headers = asyncio.run(_request("/ok", "https://evil.example"))

    assert "access-control-allow-origin" not in headers


def test_error_responses_are_not_cached(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DEBUG", raising=False)
    status, headers = asyncio.run(_request("/fail", "https://lorrgs.io"))

    assert status == 500
    assert headers["cache-control"] == "no-store"
    assert "origin" in headers["vary"].lower()
