"""08: Ansurek"""

from lorgs.models.raid_boss import RaidBoss


ANSUREK = RaidBoss(
    id=2922,
    name="Queen Ansurek",
    nick="Ansurek",
    icon="inv_achievement_raidnerubian_queenansurek.jpg",
)
boss = ANSUREK


################################################################################
# Phase 1

boss.add_cast(
    spell_id=437592,
    name="Reactive Toxin",
    duration=6,
    cooldown=5,
    color="hsl(130, 60%, 60%)",
    icon="inv_eng_bombpoison.jpg",
)

boss.add_cast(
    spell_id=443325,
    name="Infest",
    duration=1.5,
    cooldown=4.5,
    color="hsl(270, 60%, 60%)",
    icon="spell_shadow_unstableaffliction_3_purpleb.jpg",
    show=False,
)

boss.add_cast(
    spell_id=439814,
    name="Silken Tomb",
    duration=4,
    color="hsl(170, 60%, 75%)",
    icon="inv_ability_web_buff.jpg",
)

boss.add_cast(
    spell_id=437093,
    name="Feast",
    duration=1,
    color="#478fb3",
    icon="inv_misc_monsterfang_02.jpg",
    show=False,
)

boss.add_cast(
    spell_id=440899,
    name="Liquefy",
    duration=1.5,
    color="#305dd6",
    icon="ability_creature_disease_02.jpg",
    show=False,
)


################################################################################
# Phase 2

boss.add_cast(
    spell_id=447411,
    name="Wrest",
    duration=6,
    color="hsl(130, 55%, 40%)",
    icon="misc_legionfall_warlock.jpg",
    variations=[
        450191,  # Mythic P2
    ],
)

boss.add_buff(
    spell_id=447965,
    name="Gloom Touch",
    color="#dd4848",
    icon="warlock_curse_shadow_aura.jpg",
)


################################################################################
# Phase 3


boss.add_cast(
    spell_id=443336,
    name="Gorge",
    duration=2.5,
    # cooldown=45,
    color="hsl(270, 60%, 60%)",
    icon="ability_physical_taunt_purple.jpg",
)

boss.add_cast(
    spell_id=443336,
    name="Royal Condemnation",
    duration=1.5,
    cooldown=6,
    color="hsl(180, 60%, 60%)",
    icon="ability_physical_taunt_purple.jpg",
)

boss.add_cast(
    spell_id=444829,
    name="Queen's Summons",
    duration=3,
    color="hsl(50, 80%, 50%)",
    icon="inv_viciousflyingnerubian2_purple.jpg",
)

boss.add_cast(
    spell_id=443888,
    name="Abyssal Infusion",
    duration=1 + 6,
    color="hsl(300, 70%, 60%)",
    icon="inv_cosmicvoid_nova.jpg",
)

boss.add_cast(
    spell_id=445422,
    name="Frothing Gluttony",
    duration=5,
    color="hsl(100, 70%, 60%)",
    icon="ability_creature_poison_01_purple.jpg",
)


################################################################################


boss.add_phase(name="I1", spell_id=447207, event_type="applybuff")  # Predation
boss.add_phase(name="P2", spell_id=447207, event_type="removebuff")  # Predation

boss.add_phase(name="Platform 1", spell_id=448300, event_type="removebuff", count=1)  # Echoing Connection (Ascended Voidspeaker)
boss.add_phase(name="Platform 2", spell_id=462693, event_type="applybuff", count=3)  # Echoing Connection (Chamber Expeller)
boss.add_phase(name="Platform 3", spell_id=448300, event_type="applybuff", count=3)  # Echoing Connection (Ascended Voidspeaker)

boss.add_phase(name="P3", spell_id=449986, event_type="cast")
