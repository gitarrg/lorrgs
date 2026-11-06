"""WoW Forever's talent tree generator: a tiny three-tab tree, then the shipped data."""

from __future__ import annotations

import pathlib

import pytest

from lorgs.data import tab_talent_trees, talent_trees
from test.test_data.test_talent_trees import _write


def _node(node_id: int, x: int, y: int) -> dict:
    return {"ID": node_id, "TraitTreeID": 1, "PosX": x, "PosY": y, "Type": 0, "Flags": 0, "TraitSubTreeID": 0}


def _tables(tmp_path: pathlib.Path) -> dict:
    """Tree 1 with three tabs of two rows each: 10/11 (left), 20/21 (middle), 30/31 (right).

    - groups 60/61/62 are the tabs (as referenced by the "spend points" conditions)
    - groups 50/51/52 hold the second row of each tab, gated by "spend 5 points" in their tab
    - node 30 is listed right of the others with an extra digit (x=90000 for 9000), node 31 likewise (y=2000)
    """
    _write(tmp_path, "SpellName", [{"ID": 111, "Name_lang": "Spell A"}])
    _write(
        tmp_path,
        "ManifestInterfaceData",
        [{"ID": 9, "FileName": "Spell_Frost_Ring of Frost.blp", "FilePath": "Interface\\Icons\\"}],
    )
    _write(tmp_path, "SpellMisc", [{"SpellID": 111, "SpellIconFileDataID": 9, "DifficultyID": 0}])
    _write(tmp_path, "TraitCurrency", [{"ID": 7, "SourcedMax": 51}])
    _write(tmp_path, "TraitTreeXTraitCurrency", [{"ID": 1, "TraitTreeID": 1, "TraitCurrencyID": 7}])
    nodes = [_node(10, 1000, 100), _node(11, 1000, 200), _node(20, 5000, 100), _node(21, 5000, 200)]
    nodes += [_node(30, 90000, 100), _node(31, 9000, 2000), {**_node(99, 0, 0), "TraitTreeID": 2}]
    _write(tmp_path, "TraitNode", nodes)
    _write(
        tmp_path,
        "TraitNodeEntry",
        [
            {"ID": 1000 + n["ID"], "TraitDefinitionID": 1, "MaxRanks": 5, "NodeEntryType": 0, "TraitSubTreeID": 0}
            for n in nodes
        ],
    )
    _write(tmp_path, "TraitDefinition", [{"ID": 1, "SpellID": 111, "OverrideName_lang": "", "OverrideIcon": 0}])
    _write(
        tmp_path,
        "TraitNodeXTraitNodeEntry",
        [{"ID": n["ID"], "TraitNodeID": n["ID"], "TraitNodeEntryID": 1000 + n["ID"], "_Index": 0} for n in nodes],
    )
    _write(tmp_path, "TraitEdge", [{"ID": 1, "LeftTraitNodeID": 10, "RightTraitNodeID": 11}])
    members = {60: [10, 11], 61: [20, 21], 62: [30, 31], 50: [11], 51: [21], 52: [31]}
    _write(
        tmp_path,
        "TraitNodeGroupXTraitNode",
        [
            {"ID": i, "TraitNodeGroupID": g, "TraitNodeID": n}
            for i, (g, n) in enumerate((g, n) for g, ns in members.items() for n in ns)
        ],
    )
    cond = {"CondType": 0, "TraitCurrencyID": 7, "SpentAmountRequired": 5}
    _write(tmp_path, "TraitCond", [{"ID": 40 + i, "TraitNodeGroupID": 60 + i, **cond} for i in range(3)])
    _write(
        tmp_path,
        "TraitNodeGroupXTraitCond",
        [{"ID": i, "TraitCondID": 40 + i, "TraitNodeGroupID": 50 + i} for i in range(3)],
    )
    return talent_trees.read_tables(tmp_path, tab_talent_trees.TABLES)


def test_every_spec_gets_the_whole_class_tree(tmp_path: pathlib.Path) -> None:
    trees = tab_talent_trees.build_spec_trees(_tables(tmp_path), {1: [101, 102, 103]})

    assert set(trees) == {101, 102, 103}
    assert trees[101]["nodes"] == trees[103]["nodes"]
    assert trees[102]["spec_id"] == 102
    assert trees[102]["tabs"] == [101, 102, 103]
    assert trees[102]["max_points"] == 51
    assert trees[102]["edges"] == [[10, 11]]
    assert trees[102]["node_order"] == []
    assert [n["id"] for n in trees[102]["nodes"]] == [10, 11, 20, 21, 30, 31]  # not tree 2's node 99


def test_nodes_know_their_tab_and_required_points(tmp_path: pathlib.Path) -> None:
    tree = tab_talent_trees.build_spec_trees(_tables(tmp_path), {1: [101, 102, 103]})[101]
    nodes = {n["id"]: n for n in tree["nodes"]}

    assert {n: node["tab"] for n, node in nodes.items()} == {10: 0, 11: 0, 20: 1, 21: 1, 30: 2, 31: 2}
    assert {n: node["required_points"] for n, node in nodes.items()} == {10: 0, 11: 5, 20: 0, 21: 5, 30: 0, 31: 5}
    assert nodes[10] == {
        "id": 10,
        "x": 1000,
        "y": 100,
        "type": "single",
        "max_ranks": 5,
        "tree": "spec",
        "hero_tree": None,
        "hero_tree_slug": None,
        "tab": 0,
        "required_points": 0,
        "entries": [
            {"id": 1010, "name": "Spell A", "spell_id": 111, "icon": "spell_frost_ring-of-frost.jpg", "index": 0}
        ],
    }


def test_positions_with_an_extra_digit_are_fixed(tmp_path: pathlib.Path) -> None:
    tree = tab_talent_trees.build_spec_trees(_tables(tmp_path), {1: [101, 102, 103]})[101]
    nodes = {n["id"]: n for n in tree["nodes"]}

    assert (nodes[30]["x"], nodes[30]["y"]) == (9000, 100)
    assert (nodes[31]["x"], nodes[31]["y"]) == (9000, 200)


def test_a_tree_without_three_tabs_is_an_error(tmp_path: pathlib.Path) -> None:
    with pytest.raises(ValueError, match="tabs"):
        tab_talent_trees.build_spec_trees(_tables(tmp_path), {1: [101, 102]})


################################################################################
# shipped WoW Forever data
#


def test_every_forever_spec_has_a_tree() -> None:
    from lorgs.data import FOREVER

    for spec in FOREVER.data.specs:
        tree = talent_trees.get_spec_tree(FOREVER.name, spec.id)
        assert tree, spec.full_name_slug
        assert tree["max_points"] == 51
        assert tree["tabs"][spec.index - 1] == spec.id


@pytest.mark.parametrize(
    ("spec_id", "entry_id", "node_id", "tab", "name"),
    [
        # CombatantInfo `talentTree` of report xnp9L2hKMJYB1RAz, fight 1 (WoW Forever, 2026-11)
        (257, 137847, 110855, 1, "Holy Specialization"),  # priest-holy
        (257, 130579, 105850, 0, "Wand Specialization"),  # in Discipline
        (253, 129621, 104960, 0, "Deadly Aspects"),  # hunter-beastmastery
        (63, 130524, 105795, 1, "Accelerant"),  # mage-fire
        (73, 130706, 105976, 2, "Shield Specialization"),  # warrior-protection
    ],
)
def test_logged_talents_are_in_the_tree(spec_id: int, entry_id: int, node_id: int, tab: int, name: str) -> None:
    tree = talent_trees.get_spec_tree("forever", spec_id)
    assert tree
    node = next(n for n in tree["nodes"] if n["id"] == node_id)
    assert node["tab"] == tab
    assert [(e["id"], e["name"]) for e in node["entries"]] == [(entry_id, name)]
