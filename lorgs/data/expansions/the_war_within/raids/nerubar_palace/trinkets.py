from lorgs.data.retail.classes import *
from lorgs.models.wow_trinket import WowTrinket


ILVL = 639
COLOR = "#a335ee"  # Epic Items
QUERY = True


# [Aberrant Spellforge]


WowTrinket(
    spell_id=444282,
    color=COLOR,
    cooldown=90,
    name="Creeping Coagulum",
    icon="inv_raid_creepingcoagulum_purple.jpg",
    item=219917,
    ilvl=ILVL,
).add_specs(*HEAL.specs)


# [Foul Behemoth's Chelicera]


WowTrinket(
    spell_id=443124,
    color=COLOR,
    cooldown=120,
    name="Mad Queen's Mandate",
    icon="inv_raid_abyssaleffigy_purple.jpg",
    item=212454,
    ilvl=ILVL,
).add_specs(*DPS_SPECS)


# [Sikran's Endless Arsenal]


WowTrinket(
    spell_id=444489,
    color=COLOR,
    duration=20,
    name="Skyterror's Corrosive Organ",
    icon="inv_raid_oversizedacidgland_green.jpg",
    item=212453,
    ilvl=ILVL,
    query=QUERY,
).add_specs(*STR_SPECS)


WowTrinket(
    spell_id=444959,
    color="#c755f5",
    duration=20,
    name="Spymaster's Web",
    icon="inv_11_0_raid_spymastersweb_purple.jpg",
    item=220202,
    ilvl=ILVL,
).add_specs(*INT_SPECS)


# [Swarmlord's Authority]


WowTrinket(
    spell_id=449946,
    color="#8427c2",
    duration=15,
    cooldown=90,
    name="Treacherous Transmitter",
    icon="inv_etherealraid_communicator_color1.jpg",
    item=221023,
    ilvl=ILVL,
).add_specs(*ALL_SPECS)
