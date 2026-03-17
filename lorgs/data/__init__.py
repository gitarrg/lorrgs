"""All the Constant Data for Lorrgs.

In here we create all our instances for the playable Roles, Classes, Specs and list their spells.

This could be stored in a Database instead..
but at the end of the day, this was the most straight forward way and the easiest to manage.

"""

# Roles and Classes
from lorgs.data.roles import *  # noqa: F403
from lorgs.data.classes import *  # noqa: F403

from lorgs.data.racials import *  # noqa: F403
from lorgs.data.externals import *  # noqa: F403

# Consumables, Gear and similar
from lorgs.data.items import *  # noqa: F403


from lorgs.data.expansions import cataclysm  # noqa: F403
from lorgs.data.expansions import warlords_of_draenor  # noqa: F403
from lorgs.data.expansions import legion  # noqa: F403
from lorgs.data.expansions import battle_for_azeroth  # noqa: F403
from lorgs.data.expansions import shadowlands  # noqa: F403
from lorgs.data.expansions import dragonflight  # noqa: F403
from lorgs.data.expansions import the_war_within  # noqa: F403
from lorgs.data.expansions import midnight  # noqa: F403

