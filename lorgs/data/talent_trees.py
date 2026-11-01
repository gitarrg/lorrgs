"""Talent tree data per spec, generated from the DB2 tables (see `scripts/generate_talent_trees.py`).

The DB2 tree of a class holds the nodes of all its specs. Which nodes a spec has comes from
the *Visible* conditions (`TraitCond`) on the node, or on a group the node is in.
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import collections
import csv
import functools
import json
import pathlib
import re
import typing


TABLES = (
    "ChrSpecialization",
    "ManifestInterfaceData",
    "SpecSetMember",
    "SpellMisc",
    "SpellName",
    "TraitCond",
    "TraitDefinition",
    "TraitEdge",
    "TraitNode",
    "TraitNodeEntry",
    "TraitNodeGroupXTraitCond",
    "TraitNodeGroupXTraitNode",
    "TraitNodeXTraitCond",
    "TraitNodeXTraitNodeEntry",
    "TraitSubTree",
    "TraitTree",
    "TraitTreeLoadout",
)
"""DB2 tables the generator reads (`data/<name>.csv`, fetched by `data/download.sh`)."""

TREES_FILE = pathlib.Path(__file__).parent / "retail" / "talent_trees.json"

COND_TYPE_VISIBLE = "1"

MIN_HERO_TREES = 2

NODE_TYPES = {"0": "single", "1": "tiered", "2": "choice", "3": "hero_selection"}

Table = list[dict[str, str]]


def read_tables(directory: pathlib.Path) -> dict[str, Table]:
    """Read the DB2 CSVs from `directory`."""
    tables: dict[str, Table] = {}
    for name in TABLES:
        with (directory / f"{name}.csv").open(encoding="utf-8", newline="") as f:
            tables[name] = list(csv.DictReader(f))
    return tables


def _components(nodes: set[str], edges: Table) -> list[set[str]]:
    """Connected groups of `nodes`."""
    adjacent: dict[str, set[str]] = collections.defaultdict(set)
    for edge in edges:
        a, b = edge["LeftTraitNodeID"], edge["RightTraitNodeID"]
        if a in nodes and b in nodes:
            adjacent[a].add(b)
            adjacent[b].add(a)

    seen: set[str] = set()
    components: list[set[str]] = []
    for start in sorted(nodes, key=int):
        if start in seen:
            continue
        component: set[str] = set()
        todo = [start]
        while todo:
            node = todo.pop()
            if node not in component:
                component.add(node)
                todo.extend(adjacent[node])
        seen |= component
        components.append(component)
    return components


def _node_specs(tables: dict[str, Table]) -> dict[str, set[str]]:
    """Specs each node is Visible for (by the conditions on the node and on its groups)."""
    spec_sets: dict[str, set[str]] = collections.defaultdict(set)
    for row in tables["SpecSetMember"]:
        spec_sets[row["SpecSet"]].add(row["ChrSpecializationID"])

    visible_specs: dict[str, set[str]] = {}
    for cond in tables["TraitCond"]:
        if cond["CondType"] == COND_TYPE_VISIBLE and cond["SpecSetID"] != "0":
            visible_specs[cond["ID"]] = spec_sets[cond["SpecSetID"]]

    group_conds: dict[str, list[str]] = collections.defaultdict(list)
    for row in tables["TraitNodeGroupXTraitCond"]:
        group_conds[row["TraitNodeGroupID"]].append(row["TraitCondID"])
    node_conds: dict[str, list[str]] = collections.defaultdict(list)
    for row in tables["TraitNodeXTraitCond"]:
        node_conds[row["TraitNodeID"]].append(row["TraitCondID"])
    for row in tables["TraitNodeGroupXTraitNode"]:
        node_conds[row["TraitNodeID"]].extend(group_conds[row["TraitNodeGroupID"]])

    node_specs: dict[str, set[str]] = {}
    for node_id, cond_ids in node_conds.items():
        specs = set().union(*(visible_specs[c] for c in cond_ids if c in visible_specs))
        if specs:
            node_specs[node_id] = specs
    return node_specs


class _Db2:
    """Lookups shared by all specs."""

    def __init__(self, tables: dict[str, Table]) -> None:
        self.tables = tables
        self.spell_names = {r["ID"]: r["Name_lang"] for r in tables["SpellName"]}
        self.definitions = {r["ID"]: r for r in tables["TraitDefinition"]}
        self.entries = {r["ID"]: r for r in tables["TraitNodeEntry"]}
        self.sub_tree_names = {r["ID"]: r["Name_lang"] for r in tables["TraitSubTree"]}

        # icon file id -> name, as used for our spell icons: "Spell_Nature_Rejuvenation.blp" -> "spell_nature_rejuvenation.jpg"
        # Wowhead serves a space in the DB2 filename as a hyphen.
        self.icon_names = {
            r["ID"]: r["FileName"].lower().removesuffix(".blp").replace(" ", "-") + ".jpg"
            for r in tables["ManifestInterfaceData"]
            if r["FilePath"].lower() == "interface\\icons\\"
        }
        # spell id -> icon file id (spells with per-difficulty rows: the base one, DifficultyID 0, wins)
        self.spell_icons: dict[str, str] = {}
        for row in sorted(tables["SpellMisc"], key=lambda r: r["DifficultyID"] == "0"):
            self.spell_icons[row["SpellID"]] = row["SpellIconFileDataID"]

        self.nodes_by_tree: dict[str, dict[str, dict[str, str]]] = collections.defaultdict(dict)
        for row in tables["TraitNode"]:
            self.nodes_by_tree[row["TraitTreeID"]][row["ID"]] = row

        self.entries_by_node: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
        for row in sorted(tables["TraitNodeXTraitNodeEntry"], key=lambda r: int(r["_Index"])):
            self.entries_by_node[row["TraitNodeID"]].append(row)

        self.node_specs = _node_specs(tables)
        """Node id -> its specs. Nodes without a spec condition are not listed (every spec has them)."""

    def entry_data(self, node_entry_row: dict[str, str]) -> dict[str, typing.Any]:
        entry = self.entries[node_entry_row["TraitNodeEntryID"]]
        definition = self.definitions.get(entry["TraitDefinitionID"], {})
        spell_id = int(definition.get("SpellID") or 0)
        name = (
            self.spell_names.get(str(spell_id))
            or definition.get("OverrideName_lang")
            or self.sub_tree_names.get(entry["TraitSubTreeID"])
            or ""
        )
        icon_id = definition.get("OverrideIcon", "0")
        if icon_id == "0":
            icon_id = self.spell_icons.get(str(spell_id), "0")
        return {
            "id": int(entry["ID"]),
            "name": name,
            "spell_id": spell_id,
            "icon": self.icon_names.get(icon_id, ""),
            "index": int(node_entry_row["_Index"]),
        }


def hero_tree_slug(name: str) -> str:
    """Slug of a hero tree name, as used for its icon: "Elune's Chosen" -> "elunes-chosen".

    Hero tree names are unique across classes, unlike the ids of their Sub Trees (the Shaman specs have several).
    """
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace("'", "")).strip("-")


def _is_hero(node: dict[str, str]) -> bool:
    return node["TraitSubTreeID"] != "0" or node["Type"] == "3"


def _spec_nodes(db2: _Db2, spec_id: str, tree_nodes: dict[str, dict[str, str]]) -> dict[str, dict[str, str]]:
    """The nodes of one spec in the tree of its class."""
    spec_nodes = {
        node_id: node
        for node_id, node in tree_nodes.items()
        if node["TraitSubTreeID"] == "0" and spec_id in db2.node_specs.get(node_id, {spec_id})
    }

    # The spec's hero trees are the ones its hero-tree selection node offers. The conditions on a hero tree's
    # own nodes name its specs, but not reliably: some are missing (eg.: Devourer's trees can show up for a
    # Havoc), and Augmentation's Chronowarden and Scalecommander nodes name Preservation and Devastation only.
    # So take the nodes meant for the spec, unless a spec that offers the tree has far more of them.
    selection_nodes = [
        (node_id, {db2.entries[row["TraitNodeEntryID"]]["TraitSubTreeID"] for row in db2.entries_by_node[node_id]})
        for node_id, node in tree_nodes.items()
        if node["Type"] == "3"
    ]
    for sub_tree in {sub_tree for node_id, offered in selection_nodes if node_id in spec_nodes for sub_tree in offered}:
        sub_tree_nodes = {n: node for n, node in tree_nodes.items() if node["TraitSubTreeID"] == sub_tree}
        offering_specs = {spec_id}.union(
            *(db2.node_specs.get(node_id, set()) for node_id, offered in selection_nodes if sub_tree in offered),
        )
        meant_for = {
            spec: {n: node for n, node in sub_tree_nodes.items() if spec in db2.node_specs.get(n, {spec})}
            for spec in offering_specs
        }
        best = max(meant_for.values(), key=len)
        spec_nodes |= meant_for[spec_id] if 2 * len(meant_for[spec_id]) >= len(best) else best
    return spec_nodes


def _class_nodes(db2: _Db2, spec_nodes: dict[str, dict[str, str]]) -> set[str]:
    """Ids of the nodes in the class tree (the rest of the non-hero nodes are in the spec tree).

    Class and spec nodes lie in separate graphs: the leftmost one is the class tree.
    Unconnected nodes (spec roots, hidden nodes) count as class only when inside the class tree's area.
    """

    def left(node_ids: set[str]) -> int:
        return min(int(spec_nodes[n]["PosX"]) for n in node_ids)

    components = _components({n for n, node in spec_nodes.items() if not _is_hero(node)}, db2.tables["TraitEdge"])
    if not components:
        return set()
    main = min(components, key=left)
    class_right = max(int(spec_nodes[n]["PosX"]) for n in main)
    class_nodes = set(main)
    for component in components:
        if len(component) == 1 and left(component) <= class_right:
            class_nodes |= component
    return class_nodes


def _build_spec_tree(db2: _Db2, spec_id: str, tree_id: str) -> dict[str, typing.Any]:
    tree_nodes = db2.nodes_by_tree[tree_id]
    spec_nodes = _spec_nodes(db2, spec_id, tree_nodes)
    class_nodes = _class_nodes(db2, spec_nodes)

    nodes = []
    for node_id in sorted(spec_nodes, key=int):
        node = spec_nodes[node_id]
        entries = [db2.entry_data(row) for row in db2.entries_by_node[node_id]]
        max_ranks = max((int(db2.entries[str(e["id"])]["MaxRanks"]) for e in entries), default=1)
        if _is_hero(node):
            section = "hero"
        elif node_id in class_nodes:
            section = "class"
        else:
            section = "spec"
        hero_tree = db2.sub_tree_names.get(node["TraitSubTreeID"]) if section == "hero" else None
        nodes.append({
            "id": int(node_id),
            "x": int(node["PosX"]),
            "y": int(node["PosY"]),
            "type": NODE_TYPES.get(node["Type"], "single"),
            "max_ranks": max_ranks,
            "tree": section,
            "hero_tree": hero_tree,
            "hero_tree_slug": hero_tree_slug(hero_tree) if hero_tree else None,
            "entries": entries,
        })

    edges = [
        [int(e["LeftTraitNodeID"]), int(e["RightTraitNodeID"])]
        for e in db2.tables["TraitEdge"]
        if e["LeftTraitNodeID"] in spec_nodes and e["RightTraitNodeID"] in spec_nodes
    ]
    return {
        "spec_id": int(spec_id),
        "tree_id": int(tree_id),
        "nodes": nodes,
        "edges": edges,
        # The import string lists every node of the tree (not only the spec's) by id.
        "node_order": sorted(int(n) for n in tree_nodes),
    }


def build_spec_trees(tables: dict[str, Table]) -> dict[int, dict[str, typing.Any]]:
    """Build the talent tree of every spec that has one. Keyed by spec id.

    The DB2 tables keep the trees of past patches. A spec listed with several trees uses the newest (highest id)
    that has hero trees: a tree with fewer than two Sub Trees is a pre-hero-talent one.
    """
    db2 = _Db2(tables)
    real_specs = {r["ID"] for r in tables["ChrSpecialization"]}
    sub_trees_per_tree = collections.Counter(r["TraitTreeID"] for r in tables["TraitSubTree"])
    class_trees = {r["ID"] for r in tables["TraitTree"] if r["TraitSystemID"] == "0"}
    tree_of_spec: dict[str, str] = {}
    for row in tables["TraitTreeLoadout"]:
        spec_id, tree_id = row["ChrSpecializationID"], row["TraitTreeID"]
        if spec_id not in real_specs or tree_id not in class_trees or sub_trees_per_tree[tree_id] < MIN_HERO_TREES:
            continue
        if int(tree_id) > int(tree_of_spec.get(spec_id, "0")):
            tree_of_spec[spec_id] = tree_id

    return {
        int(spec): _build_spec_tree(db2, spec, tree)
        for spec, tree in sorted(tree_of_spec.items(), key=lambda i: int(i[0]))
    }


@functools.cache
def load_spec_trees() -> dict[int, dict[str, typing.Any]]:
    """The generated trees, keyed by spec id."""
    with TREES_FILE.open(encoding="utf-8") as f:
        return {int(spec_id): tree for spec_id, tree in json.load(f).items()}


def get_spec_tree(spec_id: int) -> dict[str, typing.Any] | None:
    return load_spec_trees().get(spec_id)


def get_spec_scope(spec_id: int) -> tuple[frozenset[int], dict[int, str], dict[int, int]] | None:
    """The talent entries of a spec that count for its Builds, with their hero trees and nodes.

    Hero and spec talents count; the hero tree of each hero entry; the node of each entry.
    """
    tree = get_spec_tree(spec_id)
    if tree is None:
        return None
    counted: set[int] = set()
    hero_trees: dict[int, str] = {}
    nodes: dict[int, int] = {}
    for node in tree["nodes"]:
        if node["tree"] == "class":
            continue
        for entry in node["entries"]:
            counted.add(entry["id"])
            nodes[entry["id"]] = node["id"]
            if node["hero_tree_slug"]:
                hero_trees[entry["id"]] = node["hero_tree_slug"]
    return frozenset(counted), hero_trees, nodes
