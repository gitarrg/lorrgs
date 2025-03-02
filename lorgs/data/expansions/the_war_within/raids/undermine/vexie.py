"""01: Vexie

Example Fight:
>>> scripts/load_report.py "https://www.warcraftlogs.com/reports/DzLQG1Rkp4xtdJgh?fight=10&type=casts&hostility=1&source=22"

"""

# IMPORT LOCAL LIBRARIES
from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


VEXIE = RaidBoss(
    id=3009,
    name="Vexie and the Geargrinders",
    nick="Vexie",
    icon="inv_111_raid_achievement_vexieandthegeargrinders.jpg",
)
boss = VEXIE


################################################################################
# Trinkets


GEARGRINDERS_SPARE_KEYS = boss.add_trinket(
    spell_id=0,  # TODO: on PTR the trinket's cast did not show up in logs
    cooldown=120,
    name="Geargrinder's Spare Keys",
    icon="inv_111_goblintrikekeychain_gallywix.jpg",
    item=230197,
)
"""On-Use DMG

> Use: Launch a Geargrinder trike to its final blaze of glory, exploding upon impacting
> the first enemy in its path to deal 1320420 Fire damage split between all nearby enemies. (2 Min Cooldown)
"""
GEARGRINDERS_SPARE_KEYS.add_specs(*ALL_SPECS)


VEXIES_PIT_WHISTLE = boss.add_trinket(
    spell_id=466652,
    duration=5,
    cooldown=90,
    name="Vexie's Pit Whistle",
    icon="inv_111_sapper_bilgewater.jpg",
    item=230019,
)
"""Summon Pet which explodes after 5sec

> Use: Summon Pitbot Geardo to assist you for 5 sec, coating nearby enemies
> with rancid motor oil for additional threat. Geardo ensures you take the blame.
>
> Geardo departs explosively to deal 582636 Fire damage split between nearby enemies,
> increased by 15% if recently oiled. (500ms cooldown) (1 Min, 30 Sec Cooldown)

"""
VEXIES_PIT_WHISTLE.add_specs(*STR_SPECS)
VEXIES_PIT_WHISTLE.add_specs(*AGI_SPECS)


################################################################################
# Main Phase


# Spew Oil -> spread
boss.add_cast(
    spell_id=459671,
    name="Spew Oil",
    duration=12,
    color="hsl(170, 60%, 75%)",
    icon="spell_yorsahj_bloodboil_black.jpg",
    show=False,
)

# drop fire puddles -> burn oil
boss.add_cast(
    spell_id=468207,
    name="Incendiary Fire",
    duration=6,
    color="hsl(300, 50%, 50%)",
    icon="spell_shaman_improvedfirenova.jpg",
    show=False,
)

# Exhaust Fumes --> Raid Wide AOE
boss.add_buff(
    spell_id=468149,
    name="Exhaust Fumes",
    duration=6,  # the buff stays but the dmg is only 6sec
    color="hsl(0, 50%, 50%)",
    icon="inv_misc_dust.jpg",
    event_type="applybuff, applybuffstack",
)


# Car Spawns
boss.add_cast(
    spell_id=459943,
    name="Call Bikers",
    duration=1,
    color="hsl(50, 80%, 50%)",
    icon="inv_viciousgoblintrike.jpg",
)


# Tank Buster
boss.add_cast(
    spell_id=459627,
    name="Tank Buster",
    duration=1.5,
    cooldown=25,
    color="#478fb3",
    icon="ability_vehicle_siegeenginecharge.jpg",
    show=False,
)


################################################################################
# Burn Phase

# Tune-Up / Breakdown
boss.add_debuff(
    spell_id=460603,
    name="Mechanical Breakdown",
    color="hsl(120, 70%, 50%)",
    icon="ability_siege_engineer_detonate.jpg",
)


################################################################################

boss.add_phase(name="P2 ({count})", spell_id=460116, event_type="applybuff")
boss.add_phase(name="P1 ({count})", spell_id=460116, event_type="removebuff")
