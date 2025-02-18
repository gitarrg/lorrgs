"""07: Silken Court"""

from lorgs.models.raid_boss import RaidBoss


SILKEN_COURT = RaidBoss(
    id=2921,
    name="The Silken Court",
    nick="Silken Court",
    icon="inv_achievement_raidnerubian_council.jpg",
)
boss = SILKEN_COURT


################################################################################
# Anub'arash

boss.add_cast(
    spell_id=441791,
    name="Burrowed Eruption",
    duration=1.8,
    cooldown=12,  # dot
    color="hsl(40, 60%, 50%)",
    icon="pvp_burrow.jpg",
)

boss.add_cast(
    spell_id=442994,
    name="Unleashed Swarm",
    duration=9,
    color="#bf4040",
    icon="spell_nature_insectswarm.jpg",
)

boss.add_cast(
    spell_id=438677,
    name="Stinging Swarm",
    duration=2,
    color="hsl(170, 60%, 50%)",
    icon="spell_nature_insect_swarm2.jpg",
    show=False,
)

boss.add_buff(
    spell_id=440179,
    name="Entangled",
    duration=12,
    color="hsl(300, 60%, 60%)",
    icon="inv_ability_web_buff.jpg",
)

boss.add_buff(
    spell_id=451277,
    name="Spike Storm",
    color="hsl(110, 60%, 50%)",
    icon="ability_hunter_barbedshot.jpg",
)


################################################################################
# Takazj


boss.add_cast(
    spell_id=438343,
    name="Venomous Rain",
    duration=1.5,
    cooldown=10,
    color="#6fbf40",
    icon="ability_creature_disease_03.jpg",
)

boss.add_cast(
    spell_id=441626,
    name="Web Vortex",
    duration=2,
    cooldown=16,
    color="#6fbf40",
    icon="inv_ability_web_groundstate.jpg",
)

boss.add_debuff(
    spell_id=456245,
    name="Stinging Delirium",
    duration=12,
    color="hsl(300, 60%, 60%)",
    icon="ability_creature_disease_02.jpg",
)

boss.add_buff(
    spell_id=450980,
    name="Shatter Existence",
    color="hsl(110, 60%, 50%)",
    icon="inv_cosmicvoid_wave.jpg",
)


################################################################################
# Phases

boss.add_phase(name="I1", spell_id=450980, event_type="applybuff")  # Shatter Resistance
boss.add_phase(name="P2", spell_id=450980, event_type="removebuff")  # Shatter Resistance
boss.add_phase(name="I2", spell_id=451277, event_type="applybuff")  # Spike Storm
boss.add_phase(name="P3", spell_id=451277, event_type="removebuff")  # Spike Storm
