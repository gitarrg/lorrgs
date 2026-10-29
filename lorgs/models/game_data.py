"""All the Game Data of one Game Version, indexed for lookup (ADR 0003).

A `GameData` is built once per Game Version, at import, from the objects its package defines.
It lives next to the `MemoryModel` registry for now: both hold the same objects.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import functools
import types
import typing
from collections import defaultdict

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.dungeon import Dungeon
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from lorgs.models.season import Season
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell


T = typing.TypeVar("T")

# modules outside of these prefixes are never searched for Game Data
_SHARED_PREFIX = "lorgs.data.expansions."


def _unique(objects: typing.Iterable[T]) -> list[T]:
    """Drop repeated objects (by identity), keeping the order."""
    return utils.uniqify(objects, key=id)


def _modules_of(package: types.ModuleType) -> list[types.ModuleType]:
    """The package, its imported submodules and the `expansions/` modules it imported."""
    prefix = package.__name__
    found: dict[str, types.ModuleType] = {}
    todo = [package]
    while todo:
        module = todo.pop()
        if module.__name__ in found:
            continue
        found[module.__name__] = module
        for value in vars(module).values():
            if not isinstance(value, types.ModuleType):
                continue
            if value.__name__.startswith((prefix + ".", _SHARED_PREFIX)):
                todo.append(value)
    return list(found.values())


def _members(modules: list[types.ModuleType], cls: type[T]) -> list[T]:
    """The module-level instances of `cls`."""
    return _unique(v for module in modules for v in vars(module).values() if isinstance(v, cls))


class GameData:
    """Roles, classes, specs, spells, raids, bosses, dungeons and seasons of one Game Version.

    Only the roots are stored. Everything derived from them is computed on first access.
    """

    def __init__(
        self,
        *,
        roles: list[WowRole],
        classes: list[WowClass],
        specs: list[WowSpec],
        zones: list[RaidZone],
        dungeons: list[Dungeon],
        seasons: list[Season],
        current_season: Season,
        spells: list[WowSpell] | None = None,
    ) -> None:
        self.roles = roles
        self.classes = classes
        self.specs = specs
        self.zones = zones
        self.dungeons = dungeons
        self.seasons = seasons
        self.current_season = current_season
        self.extra_spells = spells or []
        """Spells that no Actor Type holds (yet)."""

        self._link_back_references()

    @classmethod
    def from_package(cls, package: types.ModuleType, current_season: Season) -> GameData:
        """Collect everything the Game Version's package (and the `expansions/` modules it imports) defines."""
        modules = _modules_of(package)
        return cls(
            roles=_members(modules, WowRole),
            classes=_members(modules, WowClass),
            specs=_members(modules, WowSpec),
            zones=_members(modules, RaidZone),
            dungeons=_members(modules, Dungeon),
            seasons=_members(modules, Season),
            current_season=current_season,
            spells=_members(modules, WowSpell),
        )

    def _link_back_references(self) -> None:
        for role in self.roles:
            role._specs = {spec for spec in self.specs if spec.role is role}  # noqa: SLF001
        for wow_class in self.classes:
            wow_class._specs = {spec for spec in self.specs if spec.wow_class is wow_class}  # noqa: SLF001
        for zone in self.zones:
            for boss in zone.bosses:
                boss._zone = zone  # noqa: SLF001

    ####################################################################################################################
    # Derived
    ####################################################################################################################

    @functools.cached_property
    def bosses(self) -> list[RaidBoss]:
        return _unique(boss for zone in self.zones for boss in zone.bosses)

    @functools.cached_property
    def spells(self) -> list[WowSpell]:
        """Every spell an Actor Type, a zone or a dungeon holds, plus the stand-alone ones."""
        spells: list[WowSpell] = []
        for actor in (*self.classes, *self.specs, *self.bosses):
            spells += [*actor.spells, *actor.buffs, *actor.debuffs, *actor.events]
        for owner in (*self.zones, *self.dungeons, *self.bosses):
            spells += owner.trinkets
        spells += self.extra_spells
        spells += [spell.until for spell in spells if spell.until]
        return _unique(spells)

    @functools.cached_property
    def specs_by_slug(self) -> dict[str, WowSpec]:
        return {spec.full_name_slug: spec for spec in self.specs}

    @functools.cached_property
    def bosses_by_slug(self) -> dict[str, RaidBoss]:
        return {boss.full_name_slug: boss for boss in self.bosses}

    @functools.cached_property
    def bosses_by_id(self) -> dict[int, RaidBoss]:
        return {boss.id: boss for boss in self.bosses}

    @functools.cached_property
    def spells_by_id(self) -> dict[int, list[WowSpell]]:
        """Spells by their id, and by the ids of their variations."""
        index: dict[int, list[WowSpell]] = defaultdict(list)
        for spell in self.spells:
            for spell_id in {spell.spell_id, *spell.variations}:
                index[spell_id].append(spell)
        return dict(index)

    ####################################################################################################################
    # Lookups
    ####################################################################################################################

    def get_spec(self, full_name_slug: str) -> WowSpec | None:
        return self.specs_by_slug.get(full_name_slug)

    def get_boss(self, *, full_name_slug: str | None = None, boss_id: int | None = None) -> RaidBoss | None:
        if full_name_slug is not None:
            return self.bosses_by_slug.get(full_name_slug)
        return self.bosses_by_id.get(boss_id)

    def get_spells(self, spell_id: int) -> list[WowSpell]:
        """The spells with this id or with a variation of this id."""
        return self.spells_by_id.get(spell_id, [])
