"""06: One-Armed Bandit

PTR Logs:
    Mythic / Northern Sky:
    https://www.warcraftlogs.com/reports/YxpKjwFbkrC4VGv3?fight=71&type=casts&hostility=1
"""

from lorgs.data.classes import *
from lorgs.models.raid_boss import RaidBoss


ONE_ARMED_BANDIT = RaidBoss(
    id=3014,
    name="One-Armed Bandit",
    nick="Bandit",
    icon="inv_111_raid_achievement_onearmedbandit.jpg",
)
boss = ONE_ARMED_BANDIT


################################################################################
# Trinkets

GALLAGIO_BOTTLE_SERVICE = boss.add_trinket(
    spell_id=471214,
    duration=4,
    cooldown=90,
    name="Gallagio Bottle Service",
    icon="inv_111_underminegangsterdisguise.jpg",
    item=230188,
)
"""On-Use Healing (channel)

> Use: Become the pinnacle of Gallagio service excellence and dole out
> Kaja'Cola Mega-Lite to injured allies 10 times over 4 sec, healing them for
> 376075 and increasing their Speed by 1407 for 5 sec.
> The number of servings is increased by your Haste. (1 Min, 30 Sec Cooldown)

"""
GALLAGIO_BOTTLE_SERVICE.add_specs(*HEAL.specs)


HOUSE_OF_CARDS = boss.add_trinket(
    spell_id=466681,
    duration=15,
    cooldown=90,
    name="House of Cards",
    icon="inv_111_gallyjack_gallywix.jpg",
    item=23002,
)
"""On-Use mastery

Buffs:
- 466681 Mastery Buff
- 1219158 Stacked Deck

> Use: Deal yourself in, granting you 6604.2 to 8071.8 Mastery for 15 sec and
> stacking the deck. Stacking the deck increases the minimum Mastery on future
> hands by 244.6 until you leave combat, up to 3 times. (1 Min, 30 Sec Cooldown)
"""
HOUSE_OF_CARDS.add_specs(*ALL_SPECS)


################################################################################


# Pay-line
boss.add_cast(
    spell_id=460181,
    name="Pay-Line",
    duration=1 + 3,
    color="hsl(40, 70%, 50%)",
    icon="inv_10_fishing_dragonislescoins_gold.jpg",
    show=False,
)

# Heal Absorb / Vile Exhaust
boss.add_cast(
    spell_id=469993,
    name="Foul Exhaust",
    duration=5,  # not real duration
    color="hsl(280, 75%, 60%)",
    icon="inv_elemental_mote_shadow01.jpg",
)

# Tank Hit: "The Big Hit"
# Mythic = 2 Circles
boss.add_cast(
    spell_id=460472,
    name="The Big Hit",
    duration=2.5,
    cooldown=30,
    color="#478fb3",
    icon="ability_warrior_decisivestrike.jpg",
    show=False,
)


# Spin to Win = Adds
# - spawns 3/4 Adds
# - kill 2 --> pickup item and deposit to boss
# -> combination of items deposited determines next mechanic
boss.add_cast(
    spell_id=461060,
    name="Spin To Win!",
    duration=2,
    cooldown=30,
    color="hsl(120, 50%, 50%)",
    icon="achievement_battleground_templeofkotmogu_02.jpg",
    variations=[
        465309,  # Cheat to Win!
    ],
)

# Rewards
rewards = boss.add_cast(
    spell_id=464772,
    name="Reward",
    duration=10,  # idk
    color="hsl(100, 70%, 50%)",
    icon="ability_mage_fierypayback.jpg",
    variations=[
        464772,  # Reward: Shock and Flame
        464801,  # Reward: Shock and Bomb
        464804,  # Reward: Flame and Bomb
        464806,  # Reward: Flame and Coin
        464809,  # Reward: Coin and Shock
        464810,  # Reward: Coin and Bomb
    ],
)

# todo: implement something like this?
# rewards.add_variation(spell_id=464772, name="Reward: Shock and Flame", icon="ability_mage_fierypayback.jpg")
# rewards.add_variation(spell_id=464801, name="Reward: Shock and Bomb", icon="inv_eng_bombicestun.jpg")
# rewards.add_variation(spell_id=464804, name="Reward: Flame and Bomb", icon="inv_eng_bombfire.jpg")
# rewards.add_variation(spell_id=464806, name="Reward: Flame and Coin", icon="ability_creature_cursed_01.jpg")
# rewards.add_variation(spell_id=464809, name="Reward: Coin and Shock", icon="inv_misc_enggizmos_13.jpg")
# rewards.add_variation(spell_id=464810, name="Reward: Coin and Bomb", icon="inv_misc_bomb_04.jpg")


#################################################
### Phase 2


################################################################################
# Phases

boss.add_phase(name="P2", spell_id=465765, event_type="cast")  # Maintenance Cycle
