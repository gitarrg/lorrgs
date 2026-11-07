"""WoW Forever dungeons, loaded in User Reports only (never ranked).

Ids are the Warcraft Logs encounters of a whole run (zone 3000 "Dungeons"):
`{worldData{zone(id:3000){encounters{id name}}}}`.

Sorted by level range (the trailing comment), grouped in blocks of ten levels by their lower bound.
The Scarlet Monastery wings (Graveyard, Library, Armory, Cathedral) are separate encounters.
Ranges: Forever's new dungeons from the official list, the Classic ones from Classic.
"""

# IMPORT LOCAL LIBRARIES
from lorgs.models.dungeon import Dungeon


# 10-20
HALL_OF_THANES = Dungeon(id=13065, name="Hall of Thanes")  # 13-18
RAGEFIRE_CHASM = Dungeon(id=10389, name="Ragefire Chasm")  # 13-18
RUINS_OF_LORDAERON = Dungeon(id=12999, name="Ruins of Lordaeron")  # 15-20
WAILING_CAVERNS = Dungeon(id=10043, name="Wailing Caverns")  # 17-24
DEADMINES = Dungeon(id=10036, name="Deadmines")  # 17-24

# 20-30
SHADOWFANG_KEEP = Dungeon(id=10033, name="Shadowfang Keep")  # 22-30
EXCAVATION_SITE_WETLANDS = Dungeon(id=12998, name="Excavation Site: Wetlands")  # 24-29
BLACKFATHOM_DEEPS = Dungeon(id=10048, name="Blackfathom Deeps")  # 24-32
STOCKADE = Dungeon(id=10034, name="The Stockade")  # 24-32
GRAVEYARD = Dungeon(id=10302, name="Graveyard")  # 26-36
CITY_OF_DALARAN = Dungeon(id=12959, name="City of Dalaran")  # 28-33
GNOMEREGAN = Dungeon(id=10090, name="Gnomeregan")  # 29-38
RAZORFEN_KRAUL = Dungeon(id=10047, name="Razorfen Kraul")  # 29-38
LIBRARY = Dungeon(id=10303, name="Library")  # 29-39

# 30-40
ARMORY = Dungeon(id=10304, name="Armory")  # 32-42
CATHEDRAL = Dungeon(id=10305, name="Cathedral")  # 35-45
THE_DROWNED_CITY = Dungeon(id=12970, name="The Drowned City")  # 35-40
RAZORFEN_DOWNS = Dungeon(id=10129, name="Razorfen Downs")  # 37-46

# 40-50
KROLDOK_STRONGHOLD = Dungeon(id=13039, name="Krol'dok Stronghold")  # 40-45
ULDAMAN = Dungeon(id=10070, name="Uldaman")  # 41-51
ZULFARRAK = Dungeon(id=10209, name="Zul'Farrak")  # 44-54
MARAUDON = Dungeon(id=10349, name="Maraudon")  # 46-55
ALCAZ_PRISON = Dungeon(id=12994, name="Alcaz Prison")  # 48-53

# 50-60
SUNKEN_TEMPLE = Dungeon(id=10109, name="Sunken Temple")  # 50-60
BLACKROCK_DEPTHS = Dungeon(id=10230, name="Blackrock Depths")  # 52-60
BLACKMAW_HOLD = Dungeon(id=12974, name="Blackmaw Hold")  # 55-60
BLACKROCK_SPIRE = Dungeon(id=10229, name="Blackrock Spire")  # 55-60
DIRE_MAUL = Dungeon(id=10429, name="Dire Maul")  # 55-60
THE_SHAPERS_TERRACE = Dungeon(id=13001, name="The Shaper's Terrace")  # 58-60
SCHOLOMANCE = Dungeon(id=10289, name="Scholomance")  # 58-60
STRATHOLME = Dungeon(id=10329, name="Stratholme")  # 58-60


ALL_DUNGEONS = [
    # 10-20
    HALL_OF_THANES,
    RAGEFIRE_CHASM,
    RUINS_OF_LORDAERON,
    WAILING_CAVERNS,
    DEADMINES,
    # 20-30
    SHADOWFANG_KEEP,
    EXCAVATION_SITE_WETLANDS,
    BLACKFATHOM_DEEPS,
    STOCKADE,
    GRAVEYARD,
    CITY_OF_DALARAN,
    GNOMEREGAN,
    RAZORFEN_KRAUL,
    LIBRARY,
    # 30-40
    ARMORY,
    CATHEDRAL,
    THE_DROWNED_CITY,
    RAZORFEN_DOWNS,
    # 40-50
    KROLDOK_STRONGHOLD,
    ULDAMAN,
    ZULFARRAK,
    MARAUDON,
    ALCAZ_PRISON,
    # 50-60
    SUNKEN_TEMPLE,
    BLACKROCK_DEPTHS,
    BLACKMAW_HOLD,
    BLACKROCK_SPIRE,
    DIRE_MAUL,
    THE_SHAPERS_TERRACE,
    SCHOLOMANCE,
    STRATHOLME,
]
