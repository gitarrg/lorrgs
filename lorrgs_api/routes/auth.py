"""Endpoints dealing with user authentication."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import os
import typing

# IMPORT THIRD PARTY LIBRARIES
import fastapi
import jwt

# IMPORT LOCAL LIBRARIES
from lorgs.clients import discord
from lorgs.models.user import User


SECRET_KEY = os.getenv("SECRET_KEY")
if os.getenv("DEBUG"):
    SECRET_KEY = SECRET_KEY or "my-super-secret-key"

if not SECRET_KEY:
    raise RuntimeError("missing SECRET_KEY")


REDIRECT_URI = os.getenv("REDIRECT_URI") or "https://lorrgs.io/login"


router = fastapi.APIRouter()


@router.get("/token")
async def get_token(response: fastapi.Response, code: str):
    """Exchange a Authorization Code for some user info."""
    response.headers["Cache-Control"] = "no-cache"

    # get the discord access token
    user_credentials = await discord.exchange_code(code, redirect_uri=REDIRECT_URI)
    if user_credentials.get("error"):
        error = user_credentials.get("error_description") or user_credentials.get("error") or ""
        raise fastapi.HTTPException(status_code=401, detail=error)

    # load user info
    access_token: str = user_credentials.get("access_token")  # type: ignore
    info = await discord.get_user_profile(access_token)
    # try:
    # except PermissionError:
    #     raise fastapi.HTTPException(status_code=401, detail="Invalid AuthToken.")

    # find existing User or create new one
    user = User.get(discord_id=info.id) or User.first(discord_tag=info.tag) or User(discord_id=info.id)
    # if not user:
    #     raise fastapi.HTTPException(status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Invalid User.")

    # grap info from signin (in case users arn't members of the discord server)
    user.discord_id = info.id
    user.discord_tag = info.tag
    try:
        await user.refresh()
    except ValueError:
        pass
    user.save()

    # encode everything into JWT
    # converting the ID to string due to numberical issues
    token_data = {"id": str(user.discord_id)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    return {"token": token}


@router.get("/users")
async def get_user_all():
    return "many"


@router.get("/users/{user_id:str}")
async def get_user(response: fastapi.Response, user_id: str) -> dict[str, typing.Any]:
    response.headers["Cache-Control"] = f"private, max-age={60*5}"

    user = User.get(discord_id=user_id)

    if not user:
        try:
            user = User(discord_id=user_id)
            await user.refresh()
        except ValueError:
            raise fastapi.HTTPException(status_code=404, detail="User not found")
        else:
            user.save()

    return user.model_dump()


@router.get("/users/{user_id:str}/refresh")
async def user_refresh(response: fastapi.Response, user_id: str) -> dict[str, typing.Any]:

    user = User.get(discord_id=user_id)
    if not user:
        raise fastapi.HTTPException(status_code=404, detail="User not found")

    await user.refresh()
    user.save()

    response.headers["Cache-Control"] = "no-cache"
    return user.model_dump()
