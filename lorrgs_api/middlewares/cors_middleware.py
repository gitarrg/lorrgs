"""Adds a CORS Middleware."""

# IMPORT STANDARD LIBRARIES
import os

# IMPORT THIRD PARTY LIBRARIES
import fastapi
from fastapi.middleware.cors import CORSMiddleware


# TMP FIX
DEBUG = os.getenv("DEBUG")

ORIGINS = [
    "https://lorrgs.io",
    "https://*.lorrgs-frontend.pages.dev",  # CloudFlare Pages preview Builds
]
if DEBUG:
    ORIGINS.append("*")

# 32/03/2025: tmp fix
ORIGINS = ["*"]


def init(app: fastapi.FastAPI, enabled=True):

    if not enabled:
        return

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["POST", "GET", "OPTIONS"],
        allow_headers=["*"],
        max_age=3600,
    )
