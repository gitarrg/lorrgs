"""The Game Data and the Game Version of Retail."""

# IMPORT LOCAL LIBRARIES
from lorgs.data.expansions.battle_for_azeroth.dungeons.atal_dazar import MYDAS_TALISMAN
from lorgs.data.expansions.battle_for_azeroth.dungeons.mechagon_workshop import (
    INGENIOUS_MANA_BATTERY,
    MODULAR_PLATINUM_PLATING,
)
from lorgs.data.expansions.dragonflight.dungeons.dawn_of_the_infinite import (
    ECHOING_TYRSTONE,
    MIRROR_OF_FRACTURED_TOMORROWS,
)
from lorgs.data.expansions.dragonflight.dungeons.halls_of_infusion import IRIDEUS_FRAGMENT
from lorgs.data.expansions.legion.dungeons.halls_of_valor import HORN_OF_VALOR
from lorgs.data.expansions.midnight.raids.voidspire.vaelgor_ezzorak import GLOOM_SPATTERED_DREADSCALE
from lorgs.data.expansions.shadowlands.dungeons.halls_of_atonement import CURSED_STONE_IDOL, SUNBLOOD_AMETHYST
from lorgs.data.expansions.shadowlands.dungeons.theater_of_pain import GRIM_CODEX
from lorgs.data.expansions.the_war_within.dungeons.darkflame_cleft import BURIN_OF_THE_CANDLE_KING
from lorgs.data.expansions.the_war_within.dungeons.operation_floodgate import DARKFUSE_MEDICHOPPER, RINGING_RITUAL_MUD
from lorgs.data.expansions.the_war_within.dungeons.priory_of_the_sacred_flame import (
    BURSTING_LIGHTSHARD,
    SIGNET_OF_THE_PRIORY,
)
from lorgs.data.expansions.the_war_within.dungeons.the_rookery import CHARGED_STORMROOK_PLUME
from lorgs.data.expansions.the_war_within.raids.manaforge_omaga.araz import ARAZS_RITUAL_FORGE
from lorgs.data.expansions.the_war_within.raids.manaforge_omaga.loomithar import LOOMITHARS_LIVING_SILK
from lorgs.data.expansions.the_war_within.raids.manaforge_omaga.naazindhri import SOULBINDERS_EMBRACE
from lorgs.data.expansions.the_war_within.raids.manaforge_omaga.salhadaar import PERFIDIOUS_PROJECTOR
from lorgs.data.expansions.the_war_within.raids.undermine.gallywix import CHROMEBUSTIBLE_BOMB_SUIT, EYE_OF_KEZAN
from lorgs.data.expansions.the_war_within.raids.undermine.lockenstock import MISTER_LOCK_N_STALK, MISTER_PICK_ME_UP
from lorgs.data.expansions.the_war_within.raids.undermine.mugzee import MUGS_MOXIE_JUG, ZEES_THUG_HOTLINE
from lorgs.data.expansions.the_war_within.raids.undermine.one_armed_bandit import (
    GALLAGIO_BOTTLE_SERVICE,
    HOUSE_OF_CARDS,
    rewards,
)
from lorgs.data.expansions.the_war_within.raids.undermine.rik import REVERB_RADIO
from lorgs.data.expansions.the_war_within.raids.undermine.stix import SCRAPFIELD_9001
from lorgs.data.expansions.the_war_within.raids.undermine.vexie import GEARGRINDERS_SPARE_KEYS
from lorgs.data.retail.classes import (
    DEATHKNIGHT,
    DEMONHUNTER,
    DRUID,
    EVOKER,
    HUNTER,
    MAGE,
    MONK,
    OTHER,
    PALADIN,
    PRIEST,
    ROGUE,
    SHAMAN,
    WARLOCK,
    WARRIOR,
)
from lorgs.data.retail.classes.deathknight import RAISE_ALLY
from lorgs.data.retail.classes.druid import BEAR_FORM, REBIRTH
from lorgs.data.retail.classes.other import ITEM_ROLE, UTIL_ROLE
from lorgs.data.retail.classes.warlock import SOULSTONE_RESURRECTION
from lorgs.data.retail.items.midnight import (
    LIGHTFUSED_MANA_POTION,
    LIGHTS_POTENTIAL,
    LIQUID_LUSTER,
    POTION_OF_RECKLESSNESS,
    SILVERMOON_HEALTH_POTION,
)
from lorgs.data.retail.items.the_war_within import (
    Algari_Healing_Potion,
    Algari_Mana_Potion,
    Invigorating_Healing_Potion,
    Tempered_Potion,
)
from lorgs.data.retail.racials import RACIALS
from lorgs.data.retail.roles import ALL_ROLES, MIXED
from lorgs.data.retail.season import CURRENT_SEASON
from lorgs.data.retail.seasons import MIDNIGHT_SEASON1, MIDNIGHT_SEASON2, TWW_SEASON1, TWW_SEASON2, TWW_SEASON3
from lorgs.models.difficulty import RaidDifficulty
from lorgs.models.game_data import GameData
from lorgs.models.game_version import GameVersion


STANDALONE_SPELLS = [
    RAISE_ALLY,  # Raise Ally
    BEAR_FORM,  # Bear Form
    REBIRTH,  # Rebirth
    SOULSTONE_RESURRECTION,  # Soulstone
    GLOOM_SPATTERED_DREADSCALE,  # Gloom-Spattered Dreadscale
    GEARGRINDERS_SPARE_KEYS,  # Geargrinder's Spare Keys
    SCRAPFIELD_9001,  # Scrapfield 9001
    REVERB_RADIO,  # Reverb Radio
    GALLAGIO_BOTTLE_SERVICE,  # Gallagio Bottle Service
    HOUSE_OF_CARDS,  # House of Cards
    rewards,  # Reward
    MUGS_MOXIE_JUG,  # Mug's Moxie Jug
    ZEES_THUG_HOTLINE,  # Zee's Thug Hotline
    MISTER_LOCK_N_STALK,  # Mister Lock-N-Stalk
    MISTER_PICK_ME_UP,  # Mister Pick-Me-Up
    CHROMEBUSTIBLE_BOMB_SUIT,  # Chromebustible Bomb Suit
    EYE_OF_KEZAN,  # Eye of Kezan
    PERFIDIOUS_PROJECTOR,  # Perfidious Projector
    SOULBINDERS_EMBRACE,  # Soulbinder's Embrace
    LOOMITHARS_LIVING_SILK,  # Loom'ithar's Living Silk
    ARAZS_RITUAL_FORGE,  # Araz's Ritual Forge
    CHARGED_STORMROOK_PLUME,  # Charged Stormrook Plume
    BURSTING_LIGHTSHARD,  # Bursting Lightshard
    SIGNET_OF_THE_PRIORY,  # Signet of the Priory
    DARKFUSE_MEDICHOPPER,  # Darkfuse Medichopper
    RINGING_RITUAL_MUD,  # Ringing Ritual Mud
    BURIN_OF_THE_CANDLE_KING,  # Burin of the Candle King
    IRIDEUS_FRAGMENT,  # Irideus Fragment
    ECHOING_TYRSTONE,  # Echoing Tyrstone
    MIRROR_OF_FRACTURED_TOMORROWS,  # Mirror of Fractured Tomorrows
    GRIM_CODEX,  # Grim Codex
    CURSED_STONE_IDOL,  # Cursed Stone Idol
    SUNBLOOD_AMETHYST,  # Sunblood Amethyst
    INGENIOUS_MANA_BATTERY,  # Ingenious Mana Battery
    MODULAR_PLATINUM_PLATING,  # Modular Platinum Plating
    MYDAS_TALISMAN,  # My'das Talisman
    HORN_OF_VALOR,  # Horn of Valor
    SILVERMOON_HEALTH_POTION,  # Silvermoon Health Potion
    LIGHTFUSED_MANA_POTION,  # Lightfused Mana Potion
    LIGHTS_POTENTIAL,  # Light's Potential
    POTION_OF_RECKLESSNESS,  # Potion of Recklessness
    LIQUID_LUSTER,  # Liquid Luster
    Algari_Healing_Potion,  # Health Pot
    Invigorating_Healing_Potion,  # Health Pot
    Tempered_Potion,  # Tempered Potion
    Algari_Mana_Potion,  # Algari Mana Potion
]
"""Spells that no class, spec or boss holds: battle resurrections, and the trinkets and potions of every expansion."""

GAME_DATA = GameData(
    roles=[*ALL_ROLES, MIXED, ITEM_ROLE, UTIL_ROLE],
    classes=[
        DEATHKNIGHT,
        DEMONHUNTER,
        DRUID,
        EVOKER,
        HUNTER,
        MAGE,
        MONK,
        OTHER,
        PALADIN,
        PRIEST,
        ROGUE,
        SHAMAN,
        WARLOCK,
        WARRIOR,
        RACIALS,
    ],
    seasons=[MIDNIGHT_SEASON1, MIDNIGHT_SEASON2, TWW_SEASON1, TWW_SEASON2, TWW_SEASON3],
    current_season=CURRENT_SEASON,
    difficulties=(RaidDifficulty.HEROIC, RaidDifficulty.MYTHIC),
    spells=STANDALONE_SPELLS,
)

GAME_VERSION = GameVersion(
    name="retail",
    title="Retail",
    wcl_game_version=1,
    data=GAME_DATA,
)
