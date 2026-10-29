"""Seams: every Game Data object is owned by one Game Version."""

import ast
import pathlib
from itertools import combinations

from lorgs.data import GAME_VERSIONS


DATA = pathlib.Path("lorgs/data")


def _imported_expansions(game_version: str) -> set[str]:
    """The `expansions/` modules a Game Version's package imports."""
    found: set[str] = set()
    for path in (DATA / game_version).rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom) and node.module == "lorgs.data.expansions":
                found |= {alias.name for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and (node.module or "").startswith("lorgs.data.expansions."):
                found.add(node.module.split(".")[3])
    return found


def test_each_expansion_is_imported_by_one_game_version() -> None:
    owners: dict[str, list[str]] = {}
    for name in GAME_VERSIONS:
        for expansion in _imported_expansions(name):
            owners.setdefault(expansion, []).append(name)

    assert {expansion: names for expansion, names in owners.items() if len(names) > 1} == {}
    assert owners, "no expansions found"


def test_game_versions_share_no_game_data() -> None:
    """Every Game Version owns its Game Data: no object is held by two of them (ADR 0003)."""

    def owned(game_data) -> dict[str, set[int]]:
        return {
            "roles": {id(x) for x in game_data.roles},
            "classes": {id(x) for x in game_data.classes},
            "specs": {id(x) for x in game_data.specs},
            "spells": {id(x) for x in game_data.spells},
            "zones": {id(x) for x in game_data.zones},
            "bosses": {id(x) for x in game_data.bosses},
            "seasons": {id(x) for x in game_data.seasons},
        }

    for first, second in combinations(GAME_VERSIONS.values(), 2):
        a, b = owned(first.data), owned(second.data)
        shared = {kind: a[kind] & b[kind] for kind in a if a[kind] & b[kind]}
        assert not shared, f"{first.name} and {second.name} share {sorted(shared)}"
