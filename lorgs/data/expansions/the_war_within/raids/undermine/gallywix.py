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
# P1

# Frontals
boss.add_cast(
    spell_id=466340,
    name="Scatterblast Canisters",
    duration=3,
    cooldown=30,
    color="hsl(0, 50%, 50%)",
    icon="spell_mage_infernoblast.jpg",
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


########################################
# P2


# Canisters
boss.add_cast(
    spell_id=466342,
    name="Tick-Tock Canisters",
    duration=3,
    color="hsl(0, 50%, 50%)",
    icon="inv_eng_bombstonestun.jpg",
)


boss.add_buff(
    spell_id=469293,
    name="Giga Coils",
    color="hsl(200, 60%, 50%)",
    icon="inv_10_engineering_manufacturedparts_electricalparts_color1.jpg",
)


boss.add_buff(
    spell_id=1214590,
    name="TOTAL DESTRUCTION!!!",
    color="hsl(120, 50%, 50%)",
    icon="ui_majorfactions_rocket.jpg",
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

boss.add_phase(name="P2 (1)", spell_id=1216846, event_type="applybuff", count=2)  # Holding a Wrench
boss.add_phase(name="P2 (2)", spell_id=1216846, event_type="applybuff", count=4)  # Holding a Wrench
boss.add_phase(name="Int", spell_id=1214369, event_type="cast")  # TOTAL DESTRUCTION!!!
boss.add_phase(name="P3 (1)", spell_id=1214590, event_type="removebuff")  # TOTAL DESTRUCTION!!!
boss.add_phase(name="P3 (2)", spell_id=466342, event_type="cast", count=2)
boss.add_phase(name="P3 (3)", spell_id=1223658, event_type="cast", count=3)


# boss.add_phase(name="P2 (1)", spell_id=469387, event_type="applybuff")  # Carrier Giga Bomb
# boss.add_phase(name="P2 (3)", spell_id=1216846, event_type="applybuff", count=2)
# boss.add_phase(name="Int", spell_id=1214229, event_type="applybuff")  # Armageddon-class Plating
# boss.add_phase(name="P3 (2)", spell_id=466342, event_type="begincast", count=2)  # Tick-Tock Canisters
# boss.add_phase(name="P3 (3)", spell_id=1223658, event_type="cast", count=3)  # Suppression
# boss.add_phase(name="P3 (4)", spell_id=466342, event_type="begincast", count=4)  # Tick-Tock Canisters
