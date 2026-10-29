"""API-Routes to fetch static Data.

eg.: spells, classes, specs
"""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.models.wow_spec import WowSpec  # ruff: ignore[typing-only-first-party-import]
from lorgs.models.wow_spell import WowSpell  # ruff: ignore[typing-only-first-party-import]
from lorgs.models.wow_trinket import WowTrinket  # ruff: ignore[typing-only-first-party-import]
from lorrgs_api.dependencies import GameVersionDep  # ruff: ignore[typing-only-first-party-import]


router = fastapi.APIRouter()


###############################################################################
#
#       Roles
#
###############################################################################


@router.get("/roles")
async def get_roles(game_version: GameVersionDep):
    """Get all roles (tank, heal, mpds, rdps)."""
    return {"roles": [role.as_dict() for role in game_version.data.roles]}


###############################################################################
#
#       Classes
#
###############################################################################


@router.get("/classes")
async def get_classes(game_version: GameVersionDep):
    return {c.name_slug: c.as_dict() for c in game_version.data.classes}


###############################################################################
#
#       Specs
#
###############################################################################


@router.get("/specs", tags=["specs"])
async def get_specs_all(game_version: GameVersionDep) -> dict[str, list[dict]]:
    all_specs = sorted(game_version.data.specs)
    # using `as_dict()` here to prevent including the Spells/Class
    return {"specs": [spec.as_dict() for spec in all_specs]}


@router.get("/specs/{spec_slug}", tags=["specs"])
async def get_spec(game_version: GameVersionDep, spec_slug: str) -> WowSpec:
    spec = game_version.data.get_spec(spec_slug)
    if not spec:
        raise fastapi.HTTPException(status_code=404, detail="Invalid Spec.")
    return spec


@router.get("/specs/{spec_slug}/spells", tags=["specs"])
async def get_spec_spells(game_version: GameVersionDep, spec_slug: str) -> dict[int, WowSpell]:
    """Get all spells for a given spec.

    Args:
        spec_slug (str): name of the spec

    """
    spec = game_version.data.get_spec(spec_slug)
    if not spec:
        raise fastapi.HTTPException(status_code=404, detail="Invalid Spec.")

    abilities = spec.all_spells + spec.all_buffs + spec.all_debuffs + spec.all_events
    return {spell.spell_id: spell for spell in abilities}


###############################################################################
#
#       Spells
#
###############################################################################


@router.get("/spells/{spell_id}", tags=["spells"])
async def spells_one(game_version: GameVersionDep, spell_id: int) -> WowSpell:
    """Get a single Spell by spell_id."""
    spell = game_version.data.get_spell(spell_id)
    if not spell:
        raise fastapi.HTTPException(status_code=404, detail="Spell not found.")
    return spell


@router.get("/spells", tags=["spells"])
async def spells_all(game_version: GameVersionDep) -> dict[int, WowSpell]:
    """Get all Spells."""
    return {spell.spell_id: spell for spell in game_version.data.spells}


@router.get("/trinkets", tags=["spells"])
async def trinkets_all(game_version: GameVersionDep) -> dict[int, WowTrinket]:
    """Get all Trinkets."""
    return {trinket.spell_id: trinket for trinket in game_version.data.trinkets}


###############################################################################
#
#       Zones
#
###############################################################################


@router.get("/zones", tags=["raids"])
async def get_zones(game_version: GameVersionDep):
    """Get all raid-zones."""
    zones = game_version.data.zones
    return [zone.as_dict() for zone in zones]


@router.get("/zones/{zone_id}", tags=["raids"])
async def get_zone(game_version: GameVersionDep, zone_id: float):
    """Get a specific (raid-)Zone."""
    zone = game_version.data.get_zone(zone_id)
    if not zone:
        raise fastapi.HTTPException(status_code=404, detail="Invalid Zone.")
    return zone.as_dict()


@router.get("/zones/{zone_id}/bosses", tags=["raids"])
async def get_zone_bosses(game_version: GameVersionDep, zone_id: float):
    """Get all Bosses in a given Raid Zone."""
    zone = game_version.data.get_zone(zone_id)
    if not zone:
        raise fastapi.HTTPException(status_code=404, detail="Invalid Zone.")
    return {boss.name_slug: boss.as_dict() for boss in zone.bosses}


###############################################################################
#
#       Bosses
#
###############################################################################


@router.get("/bosses", tags=["raids"])
async def get_bosses(game_version: GameVersionDep):
    """Gets all Bosses.

    Warning:
        this does not filter by raid.
        use "/zone/<zone_id>/bosses" to only get the bosses for a given raid.

    """
    return {"bosses": [boss.as_dict() for boss in game_version.data.bosses]}


@router.get("/bosses/{boss_slug}", tags=["raids"])
async def get_boss(game_version: GameVersionDep, boss_slug: str):
    """Get a single Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = game_version.data.get_boss(full_name_slug=boss_slug)
    if not boss:
        raise fastapi.HTTPException(status_code=404, detail="Invalid Boss.")
    return boss.as_dict()


@router.get("/bosses/{boss_slug}/spells", tags=["raids"])
async def get_boss_spells(game_version: GameVersionDep, boss_slug: str):
    """Get Spells for a given Boss.

    Args:
        boss_slug (string): name of the boss

    """
    boss = game_version.data.get_boss(full_name_slug=boss_slug)
    if not boss:
        raise fastapi.HTTPException(status_code=404, detail="Invalid Boss.")

    spells = boss.all_spells + boss.all_buffs + boss.all_debuffs + boss.all_events
    return {spell.spell_id: spell.as_dict() for spell in spells}
