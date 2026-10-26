"""Integrity checks for raids referenced by a season."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import TYPE_CHECKING

from lorgs.models.raid_zone import RaidZone
from lorgs.models.season import Season


if TYPE_CHECKING:
    from lorgs.models.raid_boss import RaidBoss
    from lorgs.models.wow_spell import WowSpell


DATA = Path(__file__).resolve().parents[2] / "lorgs" / "data"
EXPANSIONS = DATA / "expansions"
SEASONS = DATA / "retail" / "seasons"


def _module_name(path: Path) -> str:
    return f"lorgs.data.retail.seasons.{path.stem}"


def _seasons() -> list[Season]:
    found: list[Season] = []
    seen: set[int] = set()
    for path in sorted(SEASONS.glob("*.py")):
        if path.name == "__init__.py":
            continue
        module = importlib.import_module(_module_name(path))
        for value in vars(module).values():
            if isinstance(value, Season) and id(value) not in seen:
                seen.add(id(value))
                found.append(value)
    return found


def _raids(seasons: list[Season]) -> list[RaidZone]:
    raids: list[RaidZone] = []
    seen: set[int] = set()
    for season in seasons:
        for raid in season.raids:
            if id(raid) in seen:
                continue
            seen.add(id(raid))
            raids.append(raid)
    return raids


def _raids_defined_by_expansion() -> dict[int, tuple[str, str]]:
    """Map a raid object to ``(expansion, CONST)`` from that expansion's raids package."""
    defined: dict[int, tuple[str, str]] = {}
    for path in sorted(EXPANSIONS.glob("*/raids/__init__.py")):
        expansion = path.parent.parent.name
        module = importlib.import_module(f"lorgs.data.expansions.{expansion}.raids")
        for name in getattr(module, "__all__", ()):
            value = getattr(module, name)
            if isinstance(value, RaidZone):
                defined[id(value)] = (expansion, name)
    return defined


def _icons(raid: RaidZone) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = [(raid.name, raid.icon)]
    for boss in raid.bosses:
        found.append((f"{raid.name} / {boss.name}", boss.icon))
        spells: list[WowSpell] = [*boss.spells, *boss.buffs, *boss.debuffs, *boss.events, *boss.trinkets]
        for spell in spells:
            found.append((f"{raid.name} / {boss.name} / {spell.name or spell.spell_id}", spell.icon))
    for trinket in raid.trinkets:
        found.append((f"{raid.name} / {trinket.name or trinket.spell_id}", trinket.icon))
    return found


def test_season_raids_are_exported_from_their_expansion() -> None:
    defined = _raids_defined_by_expansion()
    problems: list[str] = []
    for season in _seasons():
        for raid in season.raids:
            location = defined.get(id(raid))
            if location is None:
                problems.append(f"{season.slug}: {raid.name} is not exported from a raids package")
                continue
            expansion, name = location
            module = importlib.import_module(f"lorgs.data.expansions.{expansion}")
            exported = getattr(module, name, None)
            if name not in getattr(module, "__all__", ()) or exported is not raid:
                problems.append(f"{name} is missing from lorgs/data/expansions/{expansion}/__init__.py")
    assert problems == [], "\n".join(problems)


def test_zone_ids_are_unique() -> None:
    by_id: dict[int | float, RaidZone] = {}
    problems: list[str] = []
    for raid in _raids(_seasons()):
        other = by_id.get(raid.id)
        if other is not None and other is not raid:
            problems.append(f"zone id {raid.id} is used by {other.name!r} and {raid.name!r}")
        by_id[raid.id] = raid
    assert problems == [], "\n".join(problems)


def test_boss_ids_are_unique() -> None:
    by_id: dict[int, RaidBoss] = {}
    problems: list[str] = []
    for raid in _raids(_seasons()):
        for boss in raid.bosses:
            other = by_id.get(boss.id)
            if other is not None and other is not boss:
                problems.append(f"boss id {boss.id} is used by {other.name!r} and {boss.name!r}")
            by_id[boss.id] = boss
    assert problems == [], "\n".join(problems)


def test_icons_are_jpg_names() -> None:
    problems = [
        f"{label}: {icon!r}"
        for raid in _raids(_seasons())
        for label, icon in _icons(raid)
        if not icon.endswith(".jpg") or icon == ".jpg"
    ]
    assert problems == [], "\n".join(problems)
