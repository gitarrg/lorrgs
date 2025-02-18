"""Model to describe a User of Lorrgs."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import typing
from datetime import datetime

# IMPORT LOCAL LIBRARIES
from lorgs.clients import discord
from lorgs.models import base


LORRGS_SERVER_ID = "885638678607708172"
"""Server ID for the lorrgs discord."""


# Role IDs -> Permissions
# simple map to control who can access which modules
ROLE_PERMISSIONS = {
    "885660648510455839": ["user_reports", "dynamic_timers", "mod", "admin"],  # Arrgmin
    "885660390120362024": ["user_reports", "dynamic_timers", "mod"],  # Morrgerator
    "886595672525119538": ["user_reports", "dynamic_timers"],  # Investorrg
    "887397111975518288": ["user_reports", "dynamic_timers"],  # Contributorrg
    "908726333369110571": ["user_reports", "dynamic_timers"],  # User Reports Alpha Tester
    # special "role" for Liquid People
    "liquid": ["user_reports"],
}


class User(base.DynamoDBModel):

    discord_id: str
    """The Users discord ID (stored as string to avoid large number issues)."""

    # Discord Hame+Hash: eg.: "Arrg#2048"
    discord_tag: str = ""

    discord_avatar: str = ""

    # Role IDs
    discord_roles: list[str] = []

    extra_roles: list[str] = []

    # last time the roles have been checked
    updated: datetime = datetime.min

    # Config
    pkey: typing.ClassVar[str] = "{discord_id}"

    ################################
    # Properties
    #
    @property
    def name(self) -> str:
        """The Users Name only (eg.: Arrg#2048 -> Arrg)"""
        return self.discord_tag.split("#")[0]

    @property
    def discriminator(self) -> str:
        """The Users discriminator (eg.: Arrg#2048 -> 2048)"""
        return self.discord_tag.split("#")[-1]

    @property
    def roles(self) -> list[str]:
        """All Roles the User has."""
        return list(set(self.discord_roles + self.extra_roles))

    @property
    def permissions(self) -> set[str]:
        """All Permissions the User has."""
        permissions = set()
        for role in self.roles:
            role_permissions = ROLE_PERMISSIONS.get(role, [])
            permissions.update(role_permissions)
        return permissions

    def dict(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        return {
            **super().dict(**kwargs),
            "permissions": self.permissions,
            # aliases to keep things agnostic
            "name": self.discord_tag,
            "id": self.discord_id,
            "avatar": self.discord_avatar,
        }

    ################################
    # Methods
    #

    async def refresh(self) -> None:
        """Refresh the User Info from Discord."""

        # update discord roles / avatar
        member_info = await discord.get_member_info(server_id=LORRGS_SERVER_ID, user_id=self.discord_id)
        user_info = member_info.user

        self.discord_tag = user_info.tag
        self.discord_avatar = member_info.avatar or user_info.avatar or ""
        self.discord_roles = member_info.roles or []
        self.updated = datetime.utcnow()

    def add_extra_role(self, role: str) -> None:
        """Add an extra role to the user."""
        if role not in self.extra_roles:
            self.extra_roles = list(self.extra_roles)  # force a new list instance, to avoid it being considered "unset"
            self.extra_roles.append(role)
