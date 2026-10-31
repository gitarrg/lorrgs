"""01: Eranog."""

from lorgs.models.raid_boss import RaidBoss


ERANOG = RaidBoss(id=2587, name="Eranog", icon="achievement_raidprimalist_eranog.jpg")


ERANOG.add_cast(
    spell_id=370615,
    name="Molten Cleave",
    duration=3.5,
    color="#2695d1",
    icon="ability_rhyolith_magmaflow_wave.jpg",
)
ERANOG.add_cast(
    spell_id=396023,
    name="Incinerating Roar",
    duration=2.5,
    color="#bf3030",
    icon="ability_warrior_dragonroar.jpg",
)
ERANOG.add_cast(
    spell_id=390715,
    name="Flamerift",
    duration=1.5 + 6,
    color="#dbdb2c",
    icon="inv_misc_head_dragon_01.jpg",
)
ERANOG.add_buff(spell_id=370307, name="Collapsing Army", color="#46db2c", icon="spell_fire_elemental_totem.jpg")
