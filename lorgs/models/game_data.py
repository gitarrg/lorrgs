"""All the Game Data of one Game Version, indexed for lookup (ADR 0003).

A `GameData` is built once per Game Version, at import, in the `version.py` of its package.
Every Game Version owns its `GameData`; lookups never mix between Game Versions.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import functools
import typing
from collections import defaultdict

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.models.raid_zone import AUTO_DIFFICULTY, RaidZone
from lorgs.models.wow_spell import SpellTag, WowSpell
from lorgs.models.wow_trinket import WowTrinket


if typing.TYPE_CHECKING:
    from lorgs.models.difficulty import RaidDifficulty
    from lorgs.models.dungeon import Dungeon
    from lorgs.models.raid_boss import RaidBoss
    from lorgs.models.season import Season
    from lorgs.models.wow_class import WowClass
    from lorgs.models.wow_role import WowRole
    from lorgs.models.wow_spec import WowSpec


class GameData:  # ruff: ignore[too-many-public-methods]
    """Roles, classes, specs, spells, raids, bosses and dungeons of the current season of one Game Version.

    Only the roots are stored. Everything derived from them is computed on first access.
    Older seasons are not part of the Game Data: their raids, bosses and spells are not served.
    """

    def __init__(
        self,
        *,
        roles: list[WowRole],
        classes: list[WowClass],
        season: Season,
        difficulties: tuple[RaidDifficulty, ...],
        spells: list[WowSpell] | None = None,
    ) -> None:
        self.difficulties = difficulties
        """Difficulties we rank. The last entry is the default."""
        self.roles = roles
        self.classes = classes
        self.season = season
        """The current season. The only one a Game Version holds."""
        self.extra_spells = spells or []
        """Spells that no Actor Type holds (yet)."""

        self.season.activate()
        self._link_back_references()
        self._attach_consumables()

    def _link_back_references(self) -> None:
        for zone in self.zones:
            for boss in zone.bosses:
                boss._zone = zone  # ruff: ignore[private-member-access]

    def _attach_consumables(self) -> None:
        """Give every spec the consumables of its role. Roles are per Game Version, so Seasons only name their codes."""
        for potion in self.season.consumables:
            for spec in self.specs:
                if spec.role.code in potion.roles and potion not in spec.spells:
                    spec.add_spells(potion)

    @property
    def default_difficulty(self) -> RaidDifficulty:
        return self.difficulties[-1]

    @property
    def difficulty_names(self) -> tuple[str, ...]:
        """The difficulties as the lowercase names used in API routes, task payloads and S3 keys."""
        return tuple(difficulty.name.lower() for difficulty in self.difficulties)

    @property
    def default_difficulty_name(self) -> str:
        return self.default_difficulty.name.lower()

    ####################################################################################################################
    # Derived
    ####################################################################################################################

    @functools.cached_property
    def zones(self) -> list[RaidZone]:
        """The raids of the current season. Older ones are not part of the Game Data."""
        return self.season.raids

    @functools.cached_property
    def dungeons(self) -> list[Dungeon]:
        """The dungeons of the current season."""
        return self.season.dungeons

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
    def raid_cooldowns(self) -> list[WowSpell]:
        """The spells tagged as Raid Cooldowns."""
        return [spell for spell in self.spells if SpellTag.RAID_CD in spell.tags]

    @functools.cached_property
    def trinkets(self) -> list[WowTrinket]:
        return [spell for spell in self.spells if isinstance(spell, WowTrinket)]

    @functools.cached_property
    def specs_by_slug(self) -> dict[str, WowSpec]:
        return {spec.full_name_slug: spec for spec in self.specs}

    @functools.cached_property
    def classes_by_slug(self) -> dict[str, WowClass]:
        return {wow_class.name_slug: wow_class for wow_class in self.classes}

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

    def get_class(self, name_slug: str) -> WowClass | None:
        return self.classes_by_slug.get(name_slug)

    def find_spec(self, class_name_cap: str, spec_name_cap: str) -> WowSpec | None:
        """The spec by the PascalCase names Warcraft Logs uses, e.g. `DeathKnight` and `Blood`."""
        for spec in self.specs:
            if spec.name_slug_cap == spec_name_cap and spec.wow_class.name_slug_cap == class_name_cap:
                return spec
        return None

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

    def get_zone(self, zone_id: float) -> RaidZone | None:
        return self.zones_by_id.get(zone_id)

    def get_season(self, slug: str) -> Season | None:
        """The season by its slug, or `current`. Only the current season is known."""
        return self.season if slug in {"current", self.season.slug} else None

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
        return self.default_difficulty_name

    def difficulties_for_boss(self, boss_slug: str) -> list[str]:
        """All difficulties we rank for this Boss."""
        zone = self.zone_for_boss(boss_slug)
        if zone and zone.difficulty:
            return [zone.difficulty.name.lower()]
        return list(self.difficulty_names)
