"""09: Scalecommander Sarkareth."""

from lorgs.models.raid_boss import RaidBoss


SARKARETH = RaidBoss(
    id=2685,
    name="Scalecommander Sarkareth",
    nick="Sarkareth",
    icon="inv_achievement_raiddragon_sarkareth.jpg",
)
boss = SARKARETH

###################################### P1 ######################################

boss.add_cast(
    spell_id=402050,
    name="Searing Breath",
    duration=3 + 3,
    color="#b34747",
    icon="spell_fire_moltenblood.jpg",
)

boss.add_cast(
    spell_id=401810,
    name="Glittering Surge",
    duration=2 + 8,
    color="#2ee6e6",
    icon="ability_evoker_essenceburst2.jpg",
)

boss.add_cast(
    spell_id=401383,
    name="Oppressing Howl",
    duration=2,
    color="#8356d1",
    icon="ability_evoker_oppressingroar.jpg",
    show=False,
)

boss.add_cast(
    spell_id=401325,
    name="Burning Claws",
    duration=27,
    color="#478fb3",
    icon="inv_10_specialreagentfoozles_tuskclaw_fire.jpg",
    show=False,
)

# https://www.wowhead.com/spell=401500/scorching-bomb
# https://www.wowhead.com/spell=401642/mass-disintegrate


###################################### P2 ######################################

boss.add_cast(
    spell_id=404456,
    name="Abyssal Breath",
    duration=2.5,
    color="#b34747",
    icon="inv_cosmicvoid_missile.jpg",
)

boss.add_cast(
    spell_id=407496,
    name="Infinite Duress (Knock)",
    duration=3 + 8,  # est duration
    color="#2f97e0",
    icon="inv_cosmicvoid_debuff.jpg",
)


boss.add_cast(
    spell_id=411236,
    name="Void Claws",
    duration=28,
    color="#478fb3",
    icon="inv_cosmicvoid_wave.jpg",
    show=False,
)


# https://www.wowhead.com/spell=404403/desolate-blossom
# https://www.wowhead.com/spell=404027/void-bomb

###################################### P3 ######################################

# Meteor
boss.add_cast(
    spell_id=403517,
    name="Embrace of Nothingness (Meteor)",
    duration=8,
    color="#b34747",
    icon="spell_priest_void-blast.jpg",
)

boss.add_cast(
    spell_id=403625,
    name="Scouring Eternity (Hide)",
    duration=5.5,
    color="#30bf30",
    icon="inv_cosmicvoid_nova.jpg",
)

boss.add_cast(
    spell_id=403741,
    name="Cosmic Ascension",
    duration=1.5 + 4,
    color="#bf30bf",
    icon="spell_priest_divinestar_shadow.jpg",
)

# Void Slash (tank)
boss.add_cast(
    spell_id=408422,
    name="Void Slash",
    duration=3,  # 1sec cast + 2sec duration
    color="#478fb3",
    icon="inv_cosmicvoid_wave.jpg",
    show=False,
)

# https://www.wowhead.com/spell=405022/hurtling-barrage
