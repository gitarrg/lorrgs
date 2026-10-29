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
from lorgs.game_version import ACTIVE
from lorgs.models.dungeon import Dungeon
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import AUTO_DIFFICULTY, RaidZone
from lorgs.models.season import Season
from lorgs.models.wow_actor import WowActor
from lorgs.models.wow_class import WowClass
from lorgs.models.wow_role import WowRole
from lorgs.models.wow_spec import WowSpec
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_trinket import WowTrinket


T = typing.TypeVar("T")

# modules outside of these prefixes are never searched for Game Data
_SHARED_PREFIX = "lorgs.data.expansions."


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


def _members[T](modules: list[types.ModuleType], cls: type[T]) -> list[T]:
    """The module-level instances of `cls`."""
    return utils.uniqify(v for module in modules for v in vars(module).values() if isinstance(v, cls))


class GameData:
    """Roles, classes, specs, spells, raids, bosses, dungeons and seasons of one Game Version.

    Only the roots are stored. Everything derived from them is computed on first access.
    """

    def __init__(
        self,
        *,
        roles: list[WowRole],
        classes: list[WowClass],
        seasons: list[Season],
        current_season: Season,
        spells: list[WowSpell] | None = None,
    ) -> None:
        self.roles = roles
        self.classes = classes
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
            seasons=_members(modules, Season),
            current_season=current_season,
            spells=_members(modules, WowSpell),
        )

    def _link_back_references(self) -> None:
        for role in self.roles:
            role._specs = {spec for spec in self.specs if spec.role is role}  # ruff: ignore[private-member-access]
        for zone in self.zones:
            for boss in zone.bosses:
                boss._zone = zone  # ruff: ignore[private-member-access]

    ####################################################################################################################
    # Derived
    ####################################################################################################################

    @functools.cached_property
    def zones(self) -> list[RaidZone]:
        """The raids of the current season. Older ones are not part of the Game Data."""
        return utils.uniqify(self.current_season.raids)

    @functools.cached_property
    def dungeons(self) -> list[Dungeon]:
        """The dungeons of the current season."""
        return utils.uniqify(self.current_season.dungeons)

    @functools.cached_property
    def specs(self) -> list[WowSpec]:
        return utils.uniqify(spec for wow_class in self.classes for spec in sorted(wow_class.specs))

    @functools.cached_property
    def bosses(self) -> list[RaidBoss]:
        return utils.uniqify(boss for zone in self.zones for boss in zone.bosses)

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
        return utils.uniqify(spells)

    @functools.cached_property
    def trinkets(self) -> list[WowTrinket]:
        return [spell for spell in self.spells if isinstance(spell, WowTrinket)]

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
    def zones_by_id(self) -> dict[int | float, RaidZone]:
        return {zone.id: zone for zone in self.zones}

    @functools.cached_property
    def seasons_by_slug(self) -> dict[str, Season]:
        return {season.slug: season for season in self.seasons}

    @functools.cached_property
    def roles_by_code(self) -> dict[str, WowRole]:
        return {role.code: role for role in self.roles}

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

    def get_spell(self, spell_id: int) -> WowSpell | None:
        """The first spell with exactly this id (variations are not matched)."""
        return next((spell for spell in self.get_spells(spell_id) if spell.spell_id == spell_id), None)

    def resolve_spell_id(self, spell_id: int, event_type: str = "cast") -> int:
        """The id of the main spell, if `spell_id` is a variation of a spell with this event type."""
        for spell in self.get_spells(spell_id):
            if spell.spell_id != spell_id and event_type in spell.event_types:
                return spell.spell_id
        return spell_id

    def default_duration(self, spell_id: int) -> int:
        """The default duration of the spell in milliseconds (0 if unknown)."""
        spell = self.get_spell(spell_id)
        return int(spell.duration * 1000) if spell else 0

    def get_role(self, code: str) -> WowRole | None:
        return self.roles_by_code.get(code)

    def get_zone(self, zone_id: int | float) -> RaidZone | None:
        return self.zones_by_id.get(zone_id)

    def get_season(self, slug: str) -> Season | None:
        return self.seasons_by_slug.get(slug)

    def zone_for_boss(self, boss_slug: str) -> RaidZone | None:
        """The Zone the given Boss belongs to."""
        boss = self.get_boss(full_name_slug=boss_slug)
        return boss.zone if boss else None

    def resolve_difficulty(self, boss_slug: str, difficulty: str) -> str:
        """Replace the `auto` token with the difficulty we rank for this Boss's Zone.

        Any other value is returned unchanged.
        """
        if difficulty != AUTO_DIFFICULTY:
            return difficulty
        zone = self.zone_for_boss(boss_slug)
        if zone and zone.difficulty:
            return zone.difficulty.name.lower()
        return ACTIVE.default_difficulty_name

    def difficulties_for_boss(self, boss_slug: str) -> list[str]:
        """All difficulties we rank for this Boss."""
        zone = self.zone_for_boss(boss_slug)
        if zone and zone.difficulty:
            return [zone.difficulty.name.lower()]
        return list(ACTIVE.difficulty_names)
