"""The Talents of a ranked player, as Warcraft Logs returns them with `includeCombatantInfo`."""

from lorgs.clients.wcl.models.character_ranking import CharacterRanking


def _ranking(talents: list[dict]) -> CharacterRanking:
    return CharacterRanking.model_validate({
        "name": "Sample",
        "class": "Warrior",
        "spec": "Protection",
        "amount": 100.0,
        "duration": 60_000,
        "report": {"code": "abc", "startTime": 0, "fightID": 1},
        "startTime": 0,
        "talents": talents,
    })


def test_talents_are_node_entries_with_their_rank() -> None:
    ranking = _ranking([{"talentID": 130706, "points": 5}, {"talentID": 130699}])
    assert [(t.talentID, t.points) for t in ranking.talents] == [(130706, 5), (130699, 1)]


def test_classic_placeholder_talents_are_skipped() -> None:
    """The vanilla site returns these instead of talents; they must not fail the whole ranking."""
    ranking = _ranking([{"name": "Unknown Ability", "id": 0, "icon": "inv_axe_02.jpg"}] * 7)
    assert ranking.talents == []
