"""08: Chrome King Gallywix"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


GALLYWIX = RaidBoss(
    id=3016,
    name="Chrome King Gallywix",
    nick="Gallywix",
    icon="inv_111_raid_achievement_chromekinggallywix.jpg",
)
boss = GALLYWIX


################################################################################
# Trinkets

CHROMEBUSTIBLE_BOMB_SUIT = GALLYWIX.add_trinket(
    spell_id=466810,  # Spell and Buff ID
    cooldown=90,
    duration=20,  # 20sec or until shield consumed
    name="Chromebustible Bomb Suit",
    icon="inv_111_bombsuit_gallywix.jpg",
    item=230029,
)
"""On Use dmg reduction

> Use: Rapidly deploy the bomb suit to reduce damage taken by 75% for 20 sec or until
> 6290790 damage has been prevented.
> Upon depletion, the bomb suit detonates to deal 441294 Fire damage split between
> nearby enemies. (1 Min, 30 Sec Cooldown)
"""
CHROMEBUSTIBLE_BOMB_SUIT.add_specs(*TANK.specs)


EYE_OF_KEZAN = GALLYWIX.add_trinket(
    spell_id=0,
    cooldown=0,
    name="Eye of Kezan",
    icon="spell_azerite_essence08.jpg",
    item=230198,
)
"""Mastery + Main Stat Proc

> Equip: Your spells and abilities have a high chance to empower the Eye and
> grant you 284 <Primary Stat> up to 20 times, decaying rapidly upon leaving combat.
> While fully empowered, the Eye instead deals 64528 Fire damage to enemies or heals allies for 96796.
"""

################################################################################
# Spells


########################################
# pre

boss.add_buff(
    spell_id=1214590,
    name="TOTAL DESTRUCTION!!!",
    color="hsl(120, 50%, 50%)",
    icon="ui_majorfactions_rocket.jpg",
    variations=[
        # 1219278,  # mythic
    ],
)


########################################
# P1

# Frontals
boss.add_cast(
    spell_id=466340,
    name="Scatterblast Canisters",
    duration=3,
    cooldown=30,
    color="hsl(0, 50%, 50%)",
    icon="spell_mage_infernoblast.jpg",
    variations=[
        1218493,  # Mythic: Scatterbomb Canisters
    ],
)


boss.add_cast(
    spell_id=465952,
    name="Big Bad Buncha Bombs",
    duration=3,
    cooldown=4.5,
    color="hsl(30, 60%, 50%)",
    icon="ships_ability_bombers.jpg",
)

# Raid AoE
boss.add_cast(
    spell_id=466751,
    name="Venting Heat",
    duration=1,
    cooldown=4,
    color="hsl(20, 60%, 50%)",
    icon="ability_warlock_inferno.jpg",
    show=False,
)


boss.add_cast(
    spell_id=1217953,
    name="Giga Blast",
    color="hsl(200, 60%, 50%)",
    duration=3,
    cooldown=10,
    icon="ability_siege_engineer_magnetic_crush.jpg",
)


########################################
# Intermission

boss.add_buff(
    spell_id=1226891,
    name="Circuit Reboot",
    color="hsl(120, 50%, 50%)",
    icon="inv_eng_superchargedengine.jpg",
)

########################################
# P2


# Canisters
boss.add_cast(
    spell_id=466342,
    name="Tick-Tock Canisters",
    duration=3,
    color="hsl(0, 50%, 50%)",
    icon="inv_eng_bombstonestun.jpg",
    variations=[
        1229328,  # Mythic
    ],
)


boss.add_buff(
    spell_id=469293,
    name="Giga Coils",
    color="hsl(200, 60%, 50%)",
    icon="inv_10_engineering_manufacturedparts_electricalparts_color1.jpg",
)


boss.add_cast(
    spell_id=467182,
    name="Suppression",
    duration=1.5 + 3,
    color="hsl(20, 50%, 50%)",
    icon="ability_ironmaidens_rapidfire.jpg",
    show=False,
)


# Tank Hit
# Not sure if we'd pref to track the debuff (467064) on the tanks
boss.add_cast(
    spell_id=466958,
    name="Molten Gold Knuckles",
    duration=1.5,
    cooldown=22,
    icon="inv_misc_desecrated_leatherglove.jpg",
    color="hsl(220, 80%, 70%)",
    show=False,
)


################################################################################
# Phases

## Heroic
# TODO: can we bring these back?
# boss.add_phase(name="P2 (1)", spell_id=1216846, event_type="applybuff", count=2)  # Holding a Wrench
# boss.add_phase(name="P2 (2)", spell_id=1216846, event_type="applybuff", count=4)  # Holding a Wrench
# boss.add_phase(name="Int", spell_id=1214369, event_type="cast")  # TOTAL DESTRUCTION!!!
# boss.add_phase(name="P3 (1)", spell_id=1214590, event_type="removebuff")  # TOTAL DESTRUCTION!!!
# boss.add_phase(name="P3 (2)", spell_id=466342, event_type="cast", count=2)
# boss.add_phase(name="P3 (3)", spell_id=1223658, event_type="cast", count=3)

## Mythic
boss.add_phase(name="P1", spell_id=1214369, event_type="removebuff")  # TOTAL DESTRUCTION!!!

boss.add_phase(name="I1", spell_id=1226891, event_type="applybuff", count=1)  # Circuit Reboot
boss.add_phase(name="P2", spell_id=1226891, event_type="removebuff", count=1)

boss.add_phase(name="I2", spell_id=1226891, event_type="applybuff", count=2)  # Circuit Reboot
boss.add_phase(name="P3", spell_id=1226891, event_type="removebuff", count=2)
