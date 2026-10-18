"""Caching and Timing Middlewares."""

import os
import time

import fastapi


DEFAULT_CACHE_TIMEOUT = os.getenv("DEFAULT_CACHE_TIMEOUT") or 60 * 60  # 1h
DEFAULT_CACHE_HEADER = f"max-age={DEFAULT_CACHE_TIMEOUT}"


def init(app: fastapi.FastAPI, enabled=True):

    if not enabled:
        return

    @app.middleware("http")
    async def add_process_time_header(request: fastapi.Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = f"{process_time * 1000:.04f}ms"
        return response

    @app.middleware("http")
    async def add_default_cache_control(request: fastapi.Request, call_next):
        response = await call_next(request)
        response.headers.setdefault("Cache-Control", DEFAULT_CACHE_HEADER)
        return response
