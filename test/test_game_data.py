"""Seams: every Game Data object is owned by one Game Version."""

import ast
import pathlib

from lorgs.game_version import GAME_VERSIONS


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
