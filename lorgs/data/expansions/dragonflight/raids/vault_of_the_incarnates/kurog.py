"""06: Kurog Grimtotem."""

# fmt: off

from lorgs.models.raid_boss import RaidBoss


KUROG = RaidBoss(id=2605, name="Kurog Grimtotem", nick="Kurog", icon="achievement_raidprimalist_kurog.jpg")

# Intermission
KUROG.add_buff(spell_id=374779, name="Primal Barrier", color="#30bf30", icon="inv_10_elementalcombinedfoozles_primordial.jpg")

# Fire
KUROG.add_cast(spell_id=382563, name="Magma Burst", duration=1.5 + 10, color="#FFF", icon="ability_rhyolith_magmaflow_wave.jpg", show=False)
KUROG.add_cast(spell_id=374022, name="Searing Carnage", duration=3 + 5, color="#bf3030", icon="spell_fire_moltenblood.jpg")  # Dark Recitals

# Frost
KUROG.add_cast(spell_id=373678, name="Biting Chill", duration=10, color="#63c4c9", icon="spell_frost_arcticwinds.jpg", show=False)
KUROG.add_cast(spell_id=391019, name="Frigid Torrent", duration=2 + 4, color="#63c4c9", icon="spell_frost_ring-of-frost.jpg", show=False)
KUROG.add_cast(spell_id=372456, name="Absolute Zero", duration=2 + 6, color="#bf3030", icon="spell_frost_glacier.jpg")  # Soak

# Earth
KUROG.add_cast(spell_id=390796, name="Erupting Bedrock", duration=5, color="#bf8330", icon="spell_shaman_earthquake.jpg", show=False)
KUROG.add_cast(spell_id=391055, name="Enveloping Earth", duration=1.5, color="#bf8330", icon="inv_elementalearth2.jpg")
KUROG.add_cast(spell_id=374691, name="Seismic Rupture", duration=5, color="#bf3030", icon="spell_nature_earthquake.jpg")  # Dance
KUROG.add_cast(spell_id=391268, name="Earth Smite", duration=3, color="#62e3be", icon="ability_deathknight_brittlebones.jpg", show=False)  # Tank Hit from Adds

# Storm
KUROG.add_cast(spell_id=390920, name="Shocking Burst", duration=5, color="#30bfa0", icon="spell_nature_unrelentingstorm.jpg")
KUROG.add_cast(spell_id=373487, name="Lightning Crash", duration=5, color="#30bfa0", icon="spell_shaman_crashlightning.jpg")
KUROG.add_cast(spell_id=374215, name="Thunder Strike", duration=7, color="#bf3030", icon="ability_vehicle_electrocharge.jpg")
