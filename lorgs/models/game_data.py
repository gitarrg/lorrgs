"""All the Game Data of one Game Version, indexed for lookup (ADR 0003).

A `GameData` is built once per Game Version, at import, from the objects its package defines.
It lives next to the `MemoryModel` registry for now: both hold the same objects.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import importlib
import types
import typing
from collections import defaultdict

# IMPORT LOCAL LIBRARIES
from lorgs import game_version as game_version_module
from lorgs.models.dungeon import Dungeon
from lorgs.models.game_version import GameVersion
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
    return list({id(obj): obj for obj in objects}.values())


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
    """Roles, classes, specs, spells, raids, bosses, dungeons and seasons of one Game Version."""

    def __init__(
        self,
        game_version: GameVersion,
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
        self.game_version = game_version
        self.roles = _unique(roles)
        self.classes = _unique(classes)
        self.specs = _unique(specs)
        self.zones = _unique(zones)
        self.dungeons = _unique(dungeons)
        self.seasons = _unique(seasons)
        self.current_season = current_season

        self.bosses: list[RaidBoss] = _unique(boss for zone in self.zones for boss in zone.bosses)
        self.spells: list[WowSpell] = self._collect_spells(spells or [])

        self.specs_by_slug = {spec.full_name_slug: spec for spec in self.specs}
        self.bosses_by_slug = {boss.full_name_slug: boss for boss in self.bosses}
        self.bosses_by_id = {boss.id: boss for boss in self.bosses}

        self.spells_by_id: dict[int, list[WowSpell]] = defaultdict(list)
        """Spells by their id, and by the ids of their variations."""
        for spell in self.spells:
            for spell_id in (spell.spell_id, *spell.variations):
                if all(spell is not other for other in self.spells_by_id[spell_id]):
                    self.spells_by_id[spell_id].append(spell)

        self._link_back_references()

    ####################################################################################################################
    # Building
    ####################################################################################################################

    @classmethod
    def from_package(cls, game_version: GameVersion, package: types.ModuleType, current_season: Season) -> GameData:
        """Collect everything the Game Version's package (and the `expansions/` modules it imports) defines."""
        modules = _modules_of(package)
        return cls(
            game_version,
            roles=_members(modules, WowRole),
            classes=_members(modules, WowClass),
            specs=_members(modules, WowSpec),
            zones=_members(modules, RaidZone),
            dungeons=_members(modules, Dungeon),
            seasons=_members(modules, Season),
            current_season=current_season,
            spells=_members(modules, WowSpell),
        )

    def _collect_spells(self, extra: list[WowSpell]) -> list[WowSpell]:
        """Every spell reachable from an actor, a zone or a dungeon, plus the stand-alone `extra` ones."""
        actors: list[WowActor] = [*self.classes, *self.specs, *self.bosses]
        spells: list[WowSpell] = []
        for actor in actors:
            spells += [*actor.spells, *actor.buffs, *actor.debuffs, *actor.events]
        for owner in (*self.zones, *self.dungeons, *self.bosses):
            spells += owner.trinkets
        spells += extra
        spells += [spell.until for spell in spells if spell.until]
        return _unique(spells)

    def _link_back_references(self) -> None:
        for role in self.roles:
            role._specs = {spec for spec in self.specs if spec.role is role}  # noqa: SLF001
        for wow_class in self.classes:
            wow_class._specs = {spec for spec in self.specs if spec.wow_class is wow_class}  # noqa: SLF001
        for zone in self.zones:
            for boss in zone.bosses:
                boss._zone = zone  # noqa: SLF001

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


def get_game_data(game_version: GameVersion | None = None) -> GameData:
    """The Game Data of the given (default: the active) Game Version."""
    game_version = game_version or game_version_module.ACTIVE
    package = importlib.import_module(game_version.data_package)
    return package.GAME_DATA
