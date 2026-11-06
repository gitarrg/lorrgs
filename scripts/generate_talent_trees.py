#!/usr/bin/env -S PYTHONPATH=. uv run
"""Regenerate `lorgs/data/<game version>/talent_trees.json` from the DB2 tables (see `data/download.sh`).

- retail: from `data/*.csv` (`data/download.sh`)
- forever: from `data/wowf/*.csv` (`data/download.sh wowf`)
"""

import argparse
import pathlib

from lorgs.data import FOREVER, RETAIL, tab_talent_trees, talent_trees


DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


def retail_trees() -> dict:
    return talent_trees.build_spec_trees(talent_trees.read_tables(DATA_DIR))


def forever_trees() -> dict:
    tables = talent_trees.read_tables(DATA_DIR / "wowf", tab_talent_trees.TABLES)
    tab_specs = {
        wow_class.talent_tree_id: [spec.id for spec in sorted(wow_class.specs, key=lambda s: s.index)]
        for wow_class in FOREVER.data.classes
        if wow_class.talent_tree_id
    }
    return tab_talent_trees.build_spec_trees(tables, tab_specs)


GENERATORS = {RETAIL.name: retail_trees, FOREVER.name: forever_trees}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("game_versions", nargs="*", choices=sorted(GENERATORS), help="default: all")
    args = parser.parse_args()

    for name in args.game_versions or sorted(GENERATORS):
        trees = GENERATORS[name]()
        path = talent_trees.write_spec_trees(name, trees)
        print(f"{name}: {len(trees)} specs -> {path}")


if __name__ == "__main__":
    main()
