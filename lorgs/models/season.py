# IMPORT STANDARD LIBRARIES
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.models import base
from lorgs.models.dungeon import Dungeon
from lorgs.models.raid_zone import RaidZone
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_trinket import WowTrinket


class Season(base.MemoryModel):
    """A Season in the Game."""

    slug: str = ""

    name: str

    ilvl: int
    """Max Item Level of the Season."""

    domain: str = ""
    """wowhead domain (if different than live)"""

    raids: list[RaidZone] = []
    """Raids of the Season."""

    dungeons: list[Dungeon] = []
    """Dungeon which part of the Seasons M+ Pool."""

    @property
    def trinkets(self) -> typing.Generator[WowTrinket, None, None]:
        """All Trinkets from Raid & Dungeon"""
        for raid in self.raids:
            for boss in raid.bosses:
                yield from boss.trinkets
        for dungeon in self.dungeons:
            yield from dungeon.trinkets

    @property
    def spells(self) -> typing.Generator[WowSpell, None, None]:
        for raid in self.raids:
            for boss in raid.bosses:
                yield from boss.spells
                yield from boss.buffs
                yield from boss.debuffs

    def activate(self) -> None:

        for trinket in self.trinkets:
            trinket.ilvl = self.ilvl
            trinket.query = True

        if self.domain:
            for trinket in self.trinkets:
                trinket.wowhead_data += f"&domain={self.domain}"
            for spell in self.spells:
                spell.wowhead_data += f"&domain={self.domain}"

        for trinket in self.trinkets:
            trinket.post_init()  # regenerate wowhead_data
