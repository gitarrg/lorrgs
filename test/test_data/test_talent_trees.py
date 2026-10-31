"""Talent tree generator: a tiny tree, then the shipped data for Retail."""

from __future__ import annotations

import csv
import pathlib

from lorgs.data import talent_trees
from test.helpers import get_api_routes


def _write(directory: pathlib.Path, name: str, rows: list[dict]) -> None:
    columns = list(rows[0]) if rows else []
    with (directory / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _node(node_id: int, x: int, y: int, node_type: int = 0, sub_tree: int = 0) -> dict:
    return {
        "ID": node_id,
        "TraitTreeID": 1,
        "PosX": x,
        "PosY": y,
        "Type": node_type,
        "Flags": 0,
        "TraitSubTreeID": sub_tree,
    }


def _tables(tmp_path: pathlib.Path) -> dict:
    """One class with two specs (1: Alpha, 2: Beta). Tree 1 has:

    - 10, 11: class nodes (10 for both specs, 11 only for Beta), connected
    - 20: Alpha's spec node, 21 and 22: Beta's, connected
    - 30: hero tree selection, 31: a Hero node for tree 7
    """
    _write(tmp_path, "ChrSpecialization", [{"ID": 1}, {"ID": 2}])
    _write(
        tmp_path,
        "SpecSetMember",
        [
            {"ID": 1, "ChrSpecializationID": 1, "SpecSet": 100},
            {"ID": 2, "ChrSpecializationID": 2, "SpecSet": 200},
        ],
    )
    _write(tmp_path, "SpellName", [{"ID": 111, "Name_lang": "Spell A"}, {"ID": 222, "Name_lang": "Spell B"}])
    _write(tmp_path, "TraitTree", [{"ID": 1, "TraitSystemID": 0}])
    _write(
        tmp_path,
        "TraitTreeLoadout",
        [
            {"ID": 1, "TraitTreeID": 1, "ChrSpecializationID": 1},
            {"ID": 2, "TraitTreeID": 1, "ChrSpecializationID": 2},
            # an old tree without hero trees must not win, nor must a tree of another system
            {"ID": 3, "TraitTreeID": 0, "ChrSpecializationID": 1},
        ],
    )
    _write(
        tmp_path,
        "TraitSubTree",
        [{"ID": 7, "Name_lang": "Heroes", "TraitTreeID": 1}, {"ID": 8, "Name_lang": "Others", "TraitTreeID": 1}],
    )
    _write(
        tmp_path,
        "TraitNode",
        [
            _node(10, 1000, 100),
            _node(11, 1000, 200),
            _node(20, 11000, 100),
            _node(21, 11000, 200),
            _node(22, 11000, 300),
            _node(30, 8000, 100, node_type=3),
            _node(31, 9000, 100, sub_tree=7),
        ],
    )
    _write(
        tmp_path,
        "TraitNodeEntry",
        [
            {"ID": 1000, "TraitDefinitionID": 1, "MaxRanks": 2, "NodeEntryType": 1, "TraitSubTreeID": 0},
            {"ID": 1001, "TraitDefinitionID": 2, "MaxRanks": 1, "NodeEntryType": 1, "TraitSubTreeID": 0},
            {"ID": 1002, "TraitDefinitionID": 3, "MaxRanks": 1, "NodeEntryType": 1, "TraitSubTreeID": 7},
        ],
    )
    _write(
        tmp_path,
        "TraitDefinition",
        [
            {"ID": 1, "SpellID": 111, "OverrideName_lang": ""},
            {"ID": 2, "SpellID": 0, "OverrideName_lang": "Override"},
            {"ID": 3, "SpellID": 0, "OverrideName_lang": ""},
        ],
    )
    _write(
        tmp_path,
        "TraitNodeXTraitNodeEntry",
        [
            {"ID": 1, "TraitNodeID": 10, "TraitNodeEntryID": 1000, "_Index": 0},
            {"ID": 2, "TraitNodeID": 11, "TraitNodeEntryID": 1001, "_Index": 0},
            {"ID": 3, "TraitNodeID": 30, "TraitNodeEntryID": 1002, "_Index": 0},
        ],
    )
    _write(
        tmp_path,
        "TraitEdge",
        [
            {"ID": 1, "LeftTraitNodeID": 10, "RightTraitNodeID": 11},
            {"ID": 2, "LeftTraitNodeID": 20, "RightTraitNodeID": 21},  # across specs
            {"ID": 3, "LeftTraitNodeID": 21, "RightTraitNodeID": 22},
        ],
    )
    _write(
        tmp_path,
        "TraitCond",
        [
            {"ID": 1, "CondType": 1, "SpecSetID": 100},  # Visible for Alpha
            {"ID": 2, "CondType": 1, "SpecSetID": 200},  # Visible for Beta
            {"ID": 3, "CondType": 2, "SpecSetID": 100},  # Granted: not about membership
        ],
    )
    _write(
        tmp_path,
        "TraitNodeXTraitCond",
        [
            {"ID": 1, "TraitCondID": 2, "TraitNodeID": 11},
            {"ID": 2, "TraitCondID": 1, "TraitNodeID": 20},
            {"ID": 3, "TraitCondID": 2, "TraitNodeID": 21},
            {"ID": 4, "TraitCondID": 3, "TraitNodeID": 21},
            {"ID": 6, "TraitCondID": 2, "TraitNodeID": 22},
            {"ID": 5, "TraitCondID": 1, "TraitNodeID": 30},
        ],
    )
    _write(tmp_path, "TraitNodeGroupXTraitNode", [{"ID": 1, "TraitNodeGroupID": 5, "TraitNodeID": 10}])
    _write(tmp_path, "TraitNodeGroupXTraitCond", [{"ID": 1, "TraitCondID": 1, "TraitNodeGroupID": 5}])
    return talent_trees.read_tables(tmp_path)


def test_nodes_belong_to_their_spec_and_tree(tmp_path: pathlib.Path) -> None:
    trees = talent_trees.build_spec_trees(_tables(tmp_path))

    assert set(trees) == {1, 2}
    alpha = {n["id"]: n["tree"] for n in trees[1]["nodes"]}
    # 11, 21 and 22 are Beta's; the selection node (30) is Alpha's
    assert alpha == {10: "class", 20: "spec", 30: "hero", 31: "hero"}
    # node 10's condition comes from its group
    beta = {n["id"]: n["tree"] for n in trees[2]["nodes"]}
    assert 10 not in beta
    assert beta == {11: "class", 21: "spec", 22: "spec"}


def test_node_and_entry_data(tmp_path: pathlib.Path) -> None:
    alpha = talent_trees.build_spec_trees(_tables(tmp_path))[1]
    nodes = {n["id"]: n for n in alpha["nodes"]}

    assert nodes[10] == {
        "id": 10,
        "x": 1000,
        "y": 100,
        "type": "single",
        "max_ranks": 2,
        "tree": "class",
        "hero_tree": None,
        "entries": [{"id": 1000, "name": "Spell A", "spell_id": 111, "index": 0}],
    }
    assert nodes[30]["type"] == "hero_selection"
    assert nodes[30]["entries"][0]["name"] == "Heroes"  # no spell: named after the Sub Tree
    assert nodes[31]["hero_tree"] == "Heroes"


def test_edges_and_node_order(tmp_path: pathlib.Path) -> None:
    trees = talent_trees.build_spec_trees(_tables(tmp_path))

    assert trees[1]["edges"] == []  # the only edge among Alpha's nodes crosses to Beta
    assert trees[2]["edges"] == [[21, 22]]
    assert trees[1]["node_order"] == [10, 11, 20, 21, 22, 30, 31]  # the whole tree, not only the spec's
    assert trees[1]["spec_id"] == 1


################################################################################
# shipped Retail data
#


def test_holy_paladin_spot_check() -> None:
    tree = talent_trees.get_spec_tree(65)
    assert tree
    entries = {e["id"]: (n["tree"], e["name"], e["spell_id"]) for n in tree["nodes"] for e in n["entries"]}
    assert entries[102534] == ("spec", "Holy Shock", 20473)
    assert entries[102548] == ("spec", "Aura Mastery", 31821)

    heroes = {n["hero_tree"] for n in tree["nodes"] if n["tree"] == "hero"} - {None}
    assert heroes == {"Lightsmith", "Herald of the Sun"}
    assert {n["tree"] for n in tree["nodes"]} == {"class", "spec", "hero"}


def test_every_retail_spec_has_a_tree() -> None:
    from lorgs.data import RETAIL

    for spec in RETAIL.data.specs:
        if spec.role.playable:
            assert talent_trees.get_spec_tree(spec.id), spec.full_name_slug


def test_route_serves_one_spec_tree() -> None:
    routes = get_api_routes(
        "/api/retail/talent_trees/paladin-holy",
        "/api/retail/talent_trees/nope",
        "/api/retail/talent_trees/other-trinkets",
        "/api/mists/talent_trees/paladin-holy",
        "/api/forever/talent_trees/paladin-holy",
    )
    statuses = {path: status for path, (status, _) in routes.items()}
    assert statuses == {
        "/api/retail/talent_trees/paladin-holy": 200,
        "/api/retail/talent_trees/nope": 404,
        "/api/retail/talent_trees/other-trinkets": 404,
        "/api/mists/talent_trees/paladin-holy": 404,
        "/api/forever/talent_trees/paladin-holy": 404,
    }
    body = routes["/api/retail/talent_trees/paladin-holy"][1]
    assert body["spec_id"] == 65
    assert body["nodes"]
