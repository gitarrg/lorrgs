"""01: Gnarlroot."""

from lorgs.models.raid_boss import RaidBoss


NYMUE = RaidBoss(
    id=2708,
    name="Nymue, Weaver of the Cycle",
    nick="Nymue",
    icon="inv_achievement_raidemeralddream_dreamweaver.jpg",
)
boss = NYMUE


################################################################################
# Main Phase
#

# Continuum = AOE ????
# boss.add_cast(
#     spell_id=420846,
#     name="Continuum",
#     duration=6.5 + 10,
#     color="hsl(0, 50%, 50%)",
#     icon="inv_legion_faction_dreamweavers.jpg",
# )

# Impeding Loom = Dodge Lines from Boss


# Surging Growths = Soaks


# Viridian Rain = spread cicles on some players
boss.add_cast(
    spell_id=420907,
    name="Viridian Rain",
    duration=1.5 + 6,
    color="hsl(175, 50%, 50%)",
    icon="ability_evoker_dreamflight.jpg",
)


# Barrier Blossoms = Circle -> Area Denial == Drop Far


boss.add_cast(
    spell_id=426519,
    name="Weaver's Burden",
    duration=2 + 12,
    color="#478fb3",
    icon="inv_10_enchanting2_magicswirl_green.jpg",
    show=False,
)


################################################################################
# Intermission
#

boss.add_buff(
    spell_id=413443,
    name="Life Ward",
    color="hsl(120, 50%, 50%)",
    icon="spell_nature_skinofearth.jpg",
)
