"""05: Dathea, Ascended."""

from lorgs.models.raid_boss import RaidBoss


DATHEA = RaidBoss(
    id=2635,
    name="Dathea, Ascended",
    nick="Dathea",
    icon="achievement_raidprimalist_windelemental.jpg",
)

# Debuffs
DATHEA.add_cast(
    spell_id=391600,
    name="Conductive Mark",
    duration=15,
    color="#297bcc",
    icon="spell_shaman_staticshock.jpg",
    show=False,
)


# Tornados
DATHEA.add_cast(
    spell_id=388410,
    name="Crosswinds",
    duration=4,
    show=False,
    color="#6fd1c4",
    icon="inv_10_jewelcrafting_bg_air.jpg",
)

# Suck in
DATHEA.add_cast(
    spell_id=376943,
    name="Cyclone",
    duration=4 + 10,
    color="#cc3d3d",
    icon="creatureportrait_cyclone_nodebris.jpg",
)

# Summon Adds
DATHEA.add_cast(
    spell_id=387849,
    name="Coalescing Storm",
    duration=5 + 45,  # ~45sec in mythic
    color="#47663d",
    icon="inv_10_elementalspiritfoozles_air.jpg",
)

# Knockback
DATHEA.add_cast(
    spell_id=391382,
    name="Blowback",
    duration=4,
    color="#d18726",
    icon="inv_misc_volatileair.jpg",
)


DATHEA.add_cast(
    spell_id=375580,
    name="Zephyr Slam",  # # Tank Hit
    duration=1.5,
    color="#74f0f2",
    icon="ability_skyreach_wind_wall.jpg",
    show=False,
)
