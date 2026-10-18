import typing_extensions
from pydantic import BaseModel


class DiscordUser(BaseModel):
    """User object.

    ref: https://discord.com/developers/docs/resources/user#user-object
    """

    id: str
    username: str
    discriminator: str

    avatar: str | None = ""
    """the user's avatar hash."""

    @property
    def tag(self):
        """Users full Tag. eg.: `Arrg#2048`."""
        return f"{self.username}#{self.discriminator}"


class DiscordGuildMember(BaseModel):
    """Guild member object.

    ref: https://discord.com/developers/docs/resources/guild#guild-member-object
    """

    user: DiscordUser
    nick: str | None = ""

    roles: list[str]
    """Role IDs.

    They come in as Ints.. but due to them represting very large numbers
    I found it safer to convert them to string instead.
    """

    joined_at: str = ""  # ISO8601 timestamp

    avatar: str | None = ""


class DiscordAccessTokenResponse(typing_extensions.TypedDict):
    """Access token response.

    Ref:
        https://discord.com/developers/docs/topics/oauth2#authorization-code-grant-access-token-exchange-example

    Example Content:
        >>> {
        >>>     "access_token": "<ACCESS_TOKEN>",
        >>>     "token_type": "Bearer",
        >>>     "expires_in": 604800,
        >>>     "refresh_token": "<REFRESH_TOKEN>",
        >>>     "scope": "identify"
        >>> }
    """

    access_token: str
    token_type: str  # eg.: "Bearer",
    expires_in: int | None
    refresh_token: str | None
    scope: str | None  # eg.: "identify"


class DiscordErrorResponse(typing_extensions.TypedDict):
    error: str
    error_description: str
