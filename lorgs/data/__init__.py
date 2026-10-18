"""All the Constant Data for Lorrgs.

In here we create all our instances for the playable Roles, Classes, Specs and list their spells.

This could be stored in a Database instead..
but at the end of the day, this was the most straight forward way and the easiest to manage.

"""

# ruff: file-ignore[unused-import, unsorted-imports]


# Roles and Classes
from lorgs.data.roles import *
from lorgs.data.classes import *

from lorgs.data.racials import *
from lorgs.data.externals import *

# Consumables, Gear and similar
from lorgs.data.items import *


from lorgs.data.expansions import cataclysm
from lorgs.data.expansions import wrath_of_the_lich_king
from lorgs.data.expansions import warlords_of_draenor
from lorgs.data.expansions import legion
from lorgs.data.expansions import battle_for_azeroth
from lorgs.data.expansions import shadowlands
from lorgs.data.expansions import dragonflight
from lorgs.data.expansions import the_war_within
from lorgs.data.expansions import midnight
