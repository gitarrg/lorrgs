"""WoW Forever dungeons, loaded in User Reports only (never ranked).

Ids are the Warcraft Logs encounters of a whole run (zone 3000 "Dungeons"):
`{worldData{zone(id:3000){encounters{id name}}}}`.
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.dungeon import Dungeon


DEADMINES = Dungeon(id=10036, name="Deadmines")
WAILING_CAVERNS = Dungeon(id=10043, name="Wailing Caverns")
SHADOWFANG_KEEP = Dungeon(id=10033, name="Shadowfang Keep")
