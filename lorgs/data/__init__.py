"""All the Constant Data for Lorrgs.

In here we create all our instances for the playable Roles, Classes, Specs and list their spells.

This could be stored in a Database instead..
but at the end of the day, this was the most straight forward way and the easiest to manage.

"""

# ruff: file-ignore[non-empty-init-module]

# IMPORT STANDARD LIBRARIES
import importlib
import types

# IMPORT LOCAL LIBRARIES
from lorgs import game_version


def _load_active_game_version() -> None:
    """Import the active Game Version's package and re-export its public names."""
    package = importlib.import_module(game_version.ACTIVE.data_package)
    for name, value in vars(package).items():
        if name.startswith("_") or isinstance(value, types.ModuleType):
            continue  # skip submodules, so `lorgs.data.classes` can not be mistaken for a real module
        globals()[name] = value


_load_active_game_version()
