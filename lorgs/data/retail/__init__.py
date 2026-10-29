"""Game data of the Retail Game Version.

Registers the Classes, Specs and their spells, plus every expansion's Raids and Dungeons
Retail uses. The `lorgs.data` package loads this package when Retail is the active Game Version.
"""

# ruff: file-ignore[unused-import, unsorted-imports]


# Roles
from lorgs.data.retail.roles import *

# Classes
from lorgs.data.retail.classes import *

from lorgs.data.retail.racials import *
from lorgs.data.retail.externals import *

# Consumables, Gear and similar
from lorgs.data.retail.items import *

# Raids and Dungeons, each expansion preceded by its consumables.
# The order is the registration order of spells, which is the order of a spec's spells in the API.
from lorgs.data.expansions import cataclysm
from lorgs.data.expansions import wrath_of_the_lich_king
from lorgs.data.expansions import warlords_of_draenor
from lorgs.data.expansions import legion
from lorgs.data.expansions import battle_for_azeroth
from lorgs.data.expansions import shadowlands
from lorgs.data.expansions import dragonflight
from lorgs.data.retail.items.the_war_within import TWW_CONSUMABLES
from lorgs.data.expansions import the_war_within
from lorgs.data.retail.items.midnight import MIDNIGHT_CONSUMABLES
from lorgs.data.expansions import midnight

# Seasons
from lorgs.data.retail.season import CURRENT_SEASON

# Game Data
import sys

from lorgs.models.game_data import GameData

GAME_DATA = GameData.from_package(sys.modules[__name__], CURRENT_SEASON)
