"""01: Ulgrax"""

from lorgs.models.raid_boss import RaidBoss


ULGRAX = RaidBoss(
    id=2902,
    name="Ulgrax the Devourer",
    nick="Ulgrax",
    icon="inv_achievement_raidnerubian_nerubianhulk.jpg",
)
boss = ULGRAX


################################################################################
# Phase 1


# Venemous Lash = AoE Dmg + Dot
boss.add_cast(
    spell_id=435136,
    name="Venomous Lash",
    duration=2 + 4,  # 2sec cast + 4sec debuff
    color="#bf4040",
    icon="ability_poisonsting.jpg",
)


# Green Circles
# - Clear Spider webs
boss.add_cast(
    spell_id=435138,
    name="Digestive Acid",
    duration=2 + 6,  # 2sec cast + 6sec debuff
    color="hsl(90, 60%, 55%)",
    icon="ability_creature_disease_03.jpg",
)


# White Circle / Brutal Lashings
# - Group Soak
# - min 6 players
# - pull in after
boss.add_cast(
    spell_id=434803,
    name="Carnivorous Contest",
    duration=8,
    color="#a659a6",
    icon="ability_druid_ferociousbite.jpg",
)


# Tank Hit + Heal Reduction Debuff
boss.add_cast(
    spell_id=434697,
    name="Brutal Crush",
    duration=19,
    color="#478fb3",
    icon="inv_misc_claw_lobstrok_purple.jpg",
    show=False,
)


################################################################################
# Phase 2

# Jump to middle + AoE
boss.add_cast(
    spell_id=445123,
    name="Hulking Crash",
    duration=5,
    color="hsl(30, 50%, 60%)",
    icon="spell_nature_earthquake.jpg",
    show=False,
)


boss.add_cast(
    spell_id=436203,
    name="Juggernaut Charge",
    duration=3.7,
    color="hsl(270, 50%, 60%)",
    icon="ability_warlock_shadowfurytga.jpg",
)


boss.add_buff(
    spell_id=445052,
    name="Chittering Swarm",
    color="hsl(120, 50%, 50%)",
    icon="spell_nature_insect_swarm2.jpg",
)


boss.add_cast(
    spell_id=438012,
    name="Hungering Bellows",
    duration=3,
    color="hsl(0, 50%, 50%)",
    icon="ability_fomor_boss_shout.jpg",
    show=False,
)


################################################################################
# Phases

# "Chittering Swarm" apply
boss.add_phase(name="P2", spell_id=445052, event_type="applybuff")

# "Ready to Feed" removed --> back to P1
boss.add_phase(name="P1", spell_id=440177, event_type="removedebuff"),
