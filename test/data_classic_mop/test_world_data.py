"""Seams: with Classic MoP active, the API serves Classic MoP's world data (classes with their major cooldowns, raids and bosses; no boss spells yet)."""

from lorrgs_sqs.helpers import PAYLOAD_EXPANDERS
from test.helpers import get_api_routes


WORLD_DATA_ROUTES = ["/api/roles", "/api/classes", "/api/specs", "/api/zones", "/api/bosses", "/api/spells", "/api/trinkets", "/api/seasons/current"]

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
    assert len(routes["/api/classes"][1]) == 11
    assert len(routes["/api/specs"][1]["specs"]) == 34
    assert {zone["name_slug"]: len(zone["bosses"]) for zone in routes["/api/zones"][1]} == RAID_BOSS_COUNTS
    assert len(routes["/api/bosses"][1]["bosses"]) == sum(RAID_BOSS_COUNTS.values())
    assert routes["/api/spells"][1], "classes register their major cooldowns"
    assert routes["/api/trinkets"][1] == {}
    assert routes["/api/seasons/current"][1]["collapse_raids"] is True
    assert routes["/api/seasons/current"][1]["has_comp_modes"] is False
    assert routes["/api/roles"][1]["roles"], "roles are shared between Game Versions"


def test_current_season_has_all_raids() -> None:
    from lorgs.data import CURRENT_SEASON

    assert CURRENT_SEASON.slug == "classic_mop"
    assert [raid.name_slug for raid in CURRENT_SEASON.raids] == list(RAID_BOSS_COUNTS)


def test_bosses_have_unique_ids_and_slugs() -> None:
    from lorgs.data import CURRENT_SEASON

    bosses = [boss for raid in CURRENT_SEASON.raids for boss in raid.bosses]
    assert len({boss.id for boss in bosses}) == len(bosses)
    assert len({boss.name_slug for boss in bosses}) == len(bosses)


def test_task_keywords_expand_to_the_classes_and_raids() -> None:
    assert len(PAYLOAD_EXPANDERS["spec_slug"]) == 34
    assert len(PAYLOAD_EXPANDERS["boss_slug"]) == sum(RAID_BOSS_COUNTS.values())
    assert PAYLOAD_EXPANDERS["difficulty"]({"boss_slug": "the-stone-guard"}) == ["heroic"]


def test_every_raid_ranks_only_its_highest_difficulty() -> None:
    """WCL has Normal and Heroic (10 and 25 player) for every MoP raid, so `auto` is always Heroic."""
    from lorgs.data import CURRENT_SEASON
    from lorgs.models.raid_zone import AUTO_DIFFICULTY, RaidZone

    routes = get_api_routes("/api/zones")
    assert {zone["difficulty"] for zone in routes["/api/zones"][1]} == {"heroic"}

    for boss in (boss for raid in CURRENT_SEASON.raids for boss in raid.bosses):
        assert RaidZone.resolve_difficulty(boss.full_name_slug, AUTO_DIFFICULTY) == "heroic"
        assert RaidZone.difficulties_for_boss(boss.full_name_slug) == ["heroic"]


def test_every_spec_has_major_cooldowns() -> None:
    from lorgs.models.wow_spec import WowSpec

    for spec in WowSpec.list():
        assert spec.all_spells, f"{spec.full_name} has no spells"
        assert all(spell.cooldown >= 60 for spell in spec.all_spells), spec.full_name
