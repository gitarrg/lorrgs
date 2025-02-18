"""05: Ulgrax"""

from lorgs.models.raid_boss import RaidBoss


OVINAX = RaidBoss(
    id=2919,
    name="Broodtwister Ovi'nax",
    nick="Ovi'nax",
    icon="inv_achievement_raidnerubian_swarmmother.jpg",
)
boss = OVINAX


# boss opens container + aoe
boss.add_cast(
    spell_id=442432,
    name="Ingest Black Blood",
    duration=1 + 15,
    color="#bf4040",
    icon="inv_achievement_raidnerubian_swarmmother.jpg",
)


# Purple Circle = Break Eggs
boss.add_cast(
    spell_id=442526,
    name="Experimental Dosage",
    duration=1.5 + 6,
    color="#8917ca",
    icon="spell_deathknight_bloodplague.jpg",
)


# Grey Circle = Dispel
boss.add_cast(
    spell_id=446344,
    name="Sticky Web",
    duration=5,  # fake duration
    color="#ca17a3",
    icon="inv_ability_web_debuff.jpg",
    show=False,
)
# 446349 = Debuff
# 446351 = too close to dispel target = get rooted


# Tank Debuff
boss.add_cast(
    spell_id=443003,
    name="Volatile Concoction",
    duration=1.5 + 8,
    color="#478fb3",
    icon="spell_shadow_unstableaffliction_2.jpg",
    show=False,
)

################################################################################
# Phases

# Ingest Black Blood
boss.add_phase(spell_id=442432, event_type="cast")
