from lorgs.data.retail.classes import *
from lorgs.models.wow_trinket import WowTrinket


query = False


WowTrinket(
    spell_id=423611,
    color="#eb3838",
    duration=20,
    cooldown=120,
    name="Ashes of the Embersoul",
    icon="sha_spell_fire_felfire_nightmare.jpg",
    item=207167,
    ilvl=483,
    query=query,
).add_specs(*ALL_SPECS)


WowTrinket(
    spell_id=422303,
    color="#eb3838",
    duration=3,
    cooldown=90,
    name="Bandolier of Twisted Blades",
    icon="inv_cape_special_knifebandolier_c_01.jpg",
    item=207165,
    ilvl=483,
    query=query,
).add_specs(*AGI_SPECS)


WowTrinket(
    spell_id=422146,
    color="#eb8938",
    duration=12,
    cooldown=120,
    name="Belor'relos, the Suncaller",
    icon="inv_wand_1h_firelandsraid_d_01.jpg",
    item=207172,
    ilvl=483,
    query=query,
).add_specs(*INT_SPECS)


WowTrinket(
    spell_id=422956,
    color="#9c67f1",
    duration=18,
    cooldown=120,
    name="Nymue's Unraveling Spindle",
    icon="inv_cloth_outdooremeralddream_d_01_buckle.jpg",
    item=208615,
    ilvl=483,
    query=query,
).add_specs(*INT_SPECS)


WowTrinket(
    spell_id=422083,
    color="#5ac927",
    duration=12 + 12,  # 12sec Seed + 12sec Mastery
    cooldown=120,
    name="Smoldering Seedling",
    icon="inv_treepet.jpg",
    item=207170,
    ilvl=483,
    query=query,
).add_specs(*HEAL.specs)


WowTrinket(
    spell_id=427113,
    color="#27b1c9",
    duration=2,
    cooldown=120,
    name="Dreambinder, Loom of the Great Cycle",
    icon="inv_staff_2h_dreamweaver_d_01.jpg",
    item=208616,
    ilvl=489,
    query=query,
).add_specs(*INT_SPECS)


WowTrinket(
    spell_id=417131,
    color="#ff8000",
    duration=3,
    cooldown=120,
    name="Rage of Fyr'alath",
    icon="inv_axe_2h_fyrakk_d_01_shadowflame.jpg",
    item=206448,
    ilvl=496,
    bonus_ids=[],  # need to clear out default "mythic/epic" bonus IDs
    query=query,
).add_specs(
    *STR_DPS_SPECS,
    DEATHKNIGHT_BLOOD,
)


WowTrinket(
    spell_id=422441,
    color="#9b632a",
    # duration=5,  // "next 3 meelee attacks"... could track the buff.. but w/e
    cooldown=150,
    name="Branch of the Tormented Ancient",
    icon="inv_misc_herb_fireweedbranch.jpg",
    item=207169,
    ilvl=496,
    query=query,
).add_specs(*STR_DPS_SPECS)
