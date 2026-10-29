"""Seams: the API serves Mists's world data (classes with their major cooldowns, raids and bosses; no boss spells yet)."""

from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS
from test.helpers import get_api_routes


WORLD_DATA_ROUTES = ["/api/mists/roles", "/api/mists/classes", "/api/mists/specs", "/api/mists/zones", "/api/mists/bosses", "/api/mists/spells", "/api/mists/trinkets", "/api/mists/seasons/current"]

RAID_BOSS_COUNTS = {
    "mogushan-vaults": 6,
    "heart-of-fear": 6,
    "terrace-of-endless-spring": 4,
    "throne-of-thunder": 13,
    "siege-of-orgrimmar": 14,
}


def test_api_starts_and_serves_classes_and_raids() -> None:
    routes = get_api_routes(*WORLD_DATA_ROUTES)

    assert {route: status for route, (status, _) in routes.items()} == dict.fromkeys(routes, 200)
    assert len(routes["/api/mists/classes"][1]) == 11
    assert len(routes["/api/mists/specs"][1]["specs"]) == 34
    assert {zone["name_slug"]: len(zone["bosses"]) for zone in routes["/api/mists/zones"][1]} == RAID_BOSS_COUNTS
    assert len(routes["/api/mists/bosses"][1]["bosses"]) == sum(RAID_BOSS_COUNTS.values())
    assert routes["/api/mists/spells"][1], "classes register their major cooldowns"
    assert routes["/api/mists/trinkets"][1] == {}
    assert routes["/api/mists/roles"][1]["roles"], "every Game Version has its own roles"


def test_current_season_has_all_raids() -> None:
    from lorgs.data.mists import CURRENT_SEASON

    assert CURRENT_SEASON.slug == "mists_phase5"
    assert [raid.name_slug for raid in CURRENT_SEASON.raids] == list(RAID_BOSS_COUNTS)


def test_bosses_have_unique_ids_and_slugs() -> None:
    from lorgs.data.mists import CURRENT_SEASON

    bosses = [boss for raid in CURRENT_SEASON.raids for boss in raid.bosses]
    assert len({boss.id for boss in bosses}) == len(bosses)
    assert len({boss.name_slug for boss in bosses}) == len(bosses)


def test_task_keywords_expand_to_the_classes_and_raids() -> None:
    assert len(PAYLOAD_EXPANDERS["spec_slug"]({"game_version": "mists"})) == 34
    assert len(PAYLOAD_EXPANDERS["boss_slug"]({"game_version": "mists"})) == sum(RAID_BOSS_COUNTS.values())
    assert PAYLOAD_EXPANDERS["difficulty"]({"game_version": "mists", "boss_slug": "the-stone-guard"}) == ["heroic"]


def test_every_raid_ranks_only_its_highest_difficulty() -> None:
    """WCL has Normal and Heroic (10 and 25 player) for every MoP raid, so `auto` is always Heroic."""
    from lorgs.data.mists import CURRENT_SEASON, GAME_DATA
    from lorgs.models.raid_zone import AUTO_DIFFICULTY

    routes = get_api_routes("/api/mists/zones")
    assert {zone["difficulty"] for zone in routes["/api/mists/zones"][1]} == {"heroic"}

    for boss in (boss for raid in CURRENT_SEASON.raids for boss in raid.bosses):
        assert GAME_DATA.resolve_difficulty(boss.full_name_slug, AUTO_DIFFICULTY) == "heroic"
        assert GAME_DATA.difficulties_for_boss(boss.full_name_slug) == ["heroic"]


def test_every_spec_has_major_cooldowns() -> None:
    from lorgs.data.mists import GAME_DATA

    for spec in GAME_DATA.specs:
        assert spec.all_spells, f"{spec.full_name} has no spells"
        assert all(spell.cooldown >= 60 for spell in spec.all_spells), spec.full_name
