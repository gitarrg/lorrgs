#!/usr/bin/env -S PYTHONPATH=. uv run
"""Regenerate `lorgs/data/retail/talent_trees.json` from the DB2 tables in `data/` (see `data/download.sh`)."""

import json
import pathlib

from lorgs.data import talent_trees


DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


def main() -> None:
    trees = talent_trees.build_spec_trees(talent_trees.read_tables(DATA_DIR))
    talent_trees.TREES_FILE.write_text(json.dumps(trees, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"{len(trees)} specs -> {talent_trees.TREES_FILE}")


if __name__ == "__main__":
    main()
