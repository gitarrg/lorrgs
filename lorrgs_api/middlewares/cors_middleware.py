"""Adds a CORS Middleware."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi.middleware.cors import CORSMiddleware


ORIGINS = [
    "https://lorrgs.io",
    "https://tbc.lorrgs.io",
    "https://mists.lorrgs.io",
    "https://forever.lorrgs.io",
    "https://classic.lorrgs.io",
]

# Pages production host and preview hosts such as https://<branch>.lorrgs-frontend.pages.dev.
# allow_origins matches literally, so the wildcard has to be a regex.
ORIGIN_REGEX = r"https://([A-Za-z0-9-]+\.)?lorrgs-frontend\.pages\.dev"


def init(app: fastapi.FastAPI, *, enabled=True):

    if not enabled:
        return

    origins = list(ORIGINS)
    if os.getenv("DEBUG"):
        origins.append("*")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex=ORIGIN_REGEX,
        allow_credentials=False,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
        max_age=3600,
    )
