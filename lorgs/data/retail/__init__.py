"""Game data of the Retail Game Version.

Registers the Retail Classes, Specs and their spells, plus every expansion's Raids and Dungeons.
`version.py` builds the Game Data and the Game Version from them.
"""

# ruff: file-ignore[unused-import, unsorted-imports]

# Roles
from lorgs.data.retail.roles import *

# Classes
from lorgs.data.retail.classes import *

from lorgs.data.retail.racials import *
from lorgs.data.retail.externals import *
from lorgs.data.retail.rezzes import *

# Consumables, Gear and similar
from lorgs.data.retail.items import *

# Raids and Dungeons.
# The order is the registration order of spells, which is the order of a spec's spells in the API.
from lorgs.data.expansions import cataclysm
from lorgs.data.expansions import wrath_of_the_lich_king
from lorgs.data.expansions import warlords_of_draenor
from lorgs.data.expansions import legion
from lorgs.data.expansions import battle_for_azeroth
from lorgs.data.expansions import shadowlands
from lorgs.data.expansions import dragonflight
from lorgs.data.expansions import the_war_within
from lorgs.data.expansions import midnight

# Seasons
from lorgs.data.retail.season import CURRENT_SEASON

# Game Data
from lorgs.data.retail.version import GAME_DATA as GAME_DATA
from lorgs.data.retail.version import GAME_VERSION as GAME_VERSION
