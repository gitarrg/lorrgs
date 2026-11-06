"""WoW Forever's talent trees, generated from its DB2 tables (see `scripts/generate_talent_trees.py`).

Forever keeps the classic talent trees (three tabs per class, 51 points, a row unlocks every 5 points spent in its
tab) but stores them in the modern Trait tables, so logs name talents by node entry id, as on Retail.

- One `TraitTree` per class, holding all three tabs side by side (the class's `talent_tree_id`).
- A node's tab: the rows of a tab are unlocked by Trait Conditions "spend N points in group G", and the groups G of
  one tab overlap. Grouping the nodes by them gives the tabs; ordered left to right they are the specs in `index` order.
- A node's `required_points`: the highest such N on the groups the node is in (0 for the first row).

The trees come out in the shape of the Retail ones (`lorgs/data/talent_trees.py`), with every node in the "spec"
tree, plus `tab` and `required_points` on each node and `tabs` (spec ids by tab) and `max_points` on the tree.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import collections
import statistics
import typing

# IMPORT LOCAL LIBRARIES
from lorgs.data import talent_trees


if typing.TYPE_CHECKING:
    from lorgs.data.talent_trees import Table


TABLES = (
    "ManifestInterfaceData",
    "SpellMisc",
    "SpellName",
    "TraitCond",
    "TraitCurrency",
    "TraitDefinition",
    "TraitEdge",
    "TraitNode",
    "TraitNodeEntry",
    "TraitNodeGroupXTraitCond",
    "TraitNodeGroupXTraitNode",
    "TraitNodeXTraitNodeEntry",
    "TraitTreeXTraitCurrency",
)
"""DB2 tables the generator reads (`data/wowf/<name>.csv`, fetched by `data/download.sh wowf`)."""

TABS = 3

MISPLACED_FACTOR = 3
"""A position more than this times the tree's median is a typo with an extra digit (eg.: x=102800 for 10280)."""


def _fix_position(value: int, median: float) -> int:
    while median and value > MISPLACED_FACTOR * median:
        value //= 10
    return value


def _tabs(
    tree_nodes: dict[str, dict[str, str]], group_nodes: dict[str, set[str]], tab_groups: set[str],
) -> list[set[str]]:
    """The nodes of each tab, left to right."""
    parent = {node_id: node_id for node_id in tree_nodes}

    def root(node_id: str) -> str:
        while parent[node_id] != node_id:
            node_id = parent[node_id]
        return node_id

    for group in tab_groups:
        members = sorted(group_nodes[group] & tree_nodes.keys())
        for node_id in members[1:]:
            parent[root(node_id)] = root(members[0])

    tabs: dict[str, set[str]] = collections.defaultdict(set)
    for node_id in tree_nodes:
        tabs[root(node_id)].add(node_id)
    return sorted(tabs.values(), key=lambda nodes: min(int(tree_nodes[n]["PosX"]) for n in nodes))


class _Db2:
    """Lookups shared by all trees."""

    def __init__(self, tables: dict[str, Table]) -> None:
        self.tables = tables
        self.spell_names = {r["ID"]: r["Name_lang"] for r in tables["SpellName"]}
        self.icon_names = talent_trees.icon_names(tables)
        self.spell_icons = talent_trees.spell_icons(tables)
        self.definitions = {r["ID"]: r for r in tables["TraitDefinition"]}
        self.entries = {r["ID"]: r for r in tables["TraitNodeEntry"]}

        currencies = {r["ID"]: int(r["SourcedMax"]) for r in tables["TraitCurrency"]}
        self.max_points = {
            r["TraitTreeID"]: currencies.get(r["TraitCurrencyID"], 0) for r in tables["TraitTreeXTraitCurrency"]
        }

        self.nodes_by_tree: dict[str, dict[str, dict[str, str]]] = collections.defaultdict(dict)
        for row in tables["TraitNode"]:
            self.nodes_by_tree[row["TraitTreeID"]][row["ID"]] = row

        self.entries_by_node: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
        for row in sorted(tables["TraitNodeXTraitNodeEntry"], key=lambda r: int(r["_Index"])):
            self.entries_by_node[row["TraitNodeID"]].append(row)

        self.group_nodes: dict[str, set[str]] = collections.defaultdict(set)
        for row in tables["TraitNodeGroupXTraitNode"]:
            self.group_nodes[row["TraitNodeGroupID"]].add(row["TraitNodeID"])

        self.required, self.tab_groups = self._spend_conditions()

    def _spend_conditions(self) -> tuple[dict[str, int], set[str]]:
        """The points each node requires, and the groups the points are counted in (each in one tab)."""
        spend_conds = {
            c["ID"]: c
            for c in self.tables["TraitCond"]
            if c["TraitCurrencyID"] != "0" and c["TraitNodeGroupID"] != "0" and int(c["SpentAmountRequired"]) > 0
        }
        required: dict[str, int] = collections.defaultdict(int)
        tab_groups: set[str] = set()
        for row in self.tables["TraitNodeGroupXTraitCond"]:
            cond = spend_conds.get(row["TraitCondID"])
            if cond is None:
                continue
            tab_groups.add(cond["TraitNodeGroupID"])
            for node_id in self.group_nodes[row["TraitNodeGroupID"]]:
                required[node_id] = max(required[node_id], int(cond["SpentAmountRequired"]))
        return required, tab_groups

    def entry_data(self, row: dict[str, str]) -> dict[str, typing.Any]:
        entry = self.entries[row["TraitNodeEntryID"]]
        definition = self.definitions.get(entry["TraitDefinitionID"], {})
        spell_id = int(definition.get("SpellID") or 0)
        icon_id = definition.get("OverrideIcon", "0")
        if icon_id == "0":
            icon_id = self.spell_icons.get(str(spell_id), "0")
        return {
            "id": int(entry["ID"]),
            "name": self.spell_names.get(str(spell_id)) or definition.get("OverrideName_lang") or "",
            "spell_id": spell_id,
            "icon": self.icon_names.get(icon_id, ""),
            "index": int(row["_Index"]),
        }


def _build_tree(db2: _Db2, tree_id: int, spec_ids: list[int]) -> dict[str, typing.Any]:
    """The tree of one class, without the spec it is for."""
    tree_nodes = db2.nodes_by_tree[str(tree_id)]
    tabs = _tabs(tree_nodes, db2.group_nodes, db2.tab_groups)
    if len(tabs) != TABS or len(spec_ids) != TABS:
        msg = f"talent tree {tree_id}: {len(tabs)} tabs for specs {spec_ids}"
        raise ValueError(msg)
    tab_of = {node_id: index for index, tab in enumerate(tabs) for node_id in tab}

    median_x = statistics.median(int(n["PosX"]) for n in tree_nodes.values())
    median_y = statistics.median(int(n["PosY"]) for n in tree_nodes.values())
    nodes = []
    for node_id in sorted(tree_nodes, key=int):
        node = tree_nodes[node_id]
        entries = [db2.entry_data(row) for row in db2.entries_by_node[node_id]]
        nodes.append({
            "id": int(node_id),
            "x": _fix_position(int(node["PosX"]), median_x),
            "y": _fix_position(int(node["PosY"]), median_y),
            "type": talent_trees.NODE_TYPES.get(node["Type"], "single"),
            "max_ranks": max((int(db2.entries[str(e["id"])]["MaxRanks"]) for e in entries), default=1),
            "tree": "spec",
            "hero_tree": None,
            "hero_tree_slug": None,
            "tab": tab_of[node_id],
            "required_points": db2.required[node_id],
            "entries": entries,
        })

    edges = [
        [int(e["LeftTraitNodeID"]), int(e["RightTraitNodeID"])]
        for e in db2.tables["TraitEdge"]
        if e["LeftTraitNodeID"] in tree_nodes and e["RightTraitNodeID"] in tree_nodes
    ]
    return {
        "tree_id": tree_id,
        "tabs": list(spec_ids),
        "max_points": db2.max_points.get(str(tree_id), 0),
        "nodes": nodes,
        "edges": edges,
        "node_order": [],  # no known import string
    }


def build_spec_trees(tables: dict[str, Table], tab_specs: dict[int, list[int]]) -> dict[int, dict[str, typing.Any]]:
    """Build the talent tree of every spec, keyed by spec id.

    Each spec of a class gets the class's whole tree: a player spends points in all three tabs.

    Args:
        tables: the DB2 tables (`TABLES`).
        tab_specs: talent tree id -> the spec ids of its tabs, left to right.

    """
    db2 = _Db2(tables)
    trees: dict[int, dict[str, typing.Any]] = {}
    for tree_id, spec_ids in tab_specs.items():
        tree = _build_tree(db2, tree_id, spec_ids)
        for spec_id in spec_ids:
            trees[spec_id] = {"spec_id": spec_id, **tree}
    return dict(sorted(trees.items()))
