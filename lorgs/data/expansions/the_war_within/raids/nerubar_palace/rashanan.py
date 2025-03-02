"""04: RASHANAN"""

from lorgs.models.raid_boss import RaidBoss


RASHANAN = RaidBoss(
    id=2918,
    name="Rasha'nan",
    icon="inv_achievement_raidnerubian_flyingnerubianevolved.jpg",
)
boss = RASHANAN


# AOE + Dot
boss.add_cast(
    spell_id=439811,
    name="Erosive Spray",
    duration=1.5 + 4,  # cast + channel
    cooldown=24,  # dot 440193
    color="#bf4040",
    icon="inv_ability_poison_missile.jpg",
)


# grey circles on random players --> leaves webs = drop far away
boss.add_cast(
    spell_id=439784,
    name="Spinneret's Strands",
    duration=2,
    color="hsl(190, 20%, 70%)",
    icon="inv_ability_web_beam.jpg",
)

# 439783 Initial Circle (4 players)
# 456170 Sticky Web --> small raid wide aoe when broken (402k)


# green lines --> soft side out
boss.add_cast(
    spell_id=439789,
    name="Rolling Acid",
    duration=2,
    color="hsl(75, 75%, 60%)",
    icon="inv_ability_poison_wave.jpg",
    show=False,
)

# 439790 Waves on 2 players
# 439785 / Corrosion = hit by wave (?)


# green circles --> small aoe + spawns adds
boss.add_cast(
    spell_id=455373,
    name="Infested Spawn",
    duration=2.5,
    cooldown=2.5,
    color="hsl(50, 75%, 50.00%)",
    icon="inv_minespider2_jungle.jpg",
    show=False,
)
# 455287 = Getting eaten by Adds


# full energy --> boss moves to another spot
boss.add_cast(
    spell_id=452806,
    name="Acidic Eruption",
    duration=2.5,
    color="hsl(75, 75%, 60%)",
    icon="inv_ability_poison_orb.jpg",
    event_type="begincast",  # Should get kicked
)


# big white circle = grp soak
boss.add_cast(
    spell_id=439795,
    name="Web Reave",
    duration=4,
    color="hsl(315, 50%, 50%)",
    icon="inv_ability_web_wave.jpg",
)


# Tank Hit?
boss.add_cast(
    spell_id=444687,
    name="Savage Assault",
    duration=1.5,
    color="#478fb3",
    icon="ability_faultline.jpg",
    show=False,
)

"""

## Erosive Spray = big AoE
  - every 30sec or so
    Debuff `440193` = raid wide dot after AoE

## Web Reave
- Grp Soak + Grip danach (mehr spieler = weniger grip)

## Spinneret's Strands
    - `439783` = Grey Circle on some players
    - `456170` = debuff nach dem ablegen / solange man mit der Flaeche verbunden ist
    --> small Raid Wide AoE wenn connection gebrochen wird

## Rolling Acid:
`439790` = Debuff auf Playern die die Waves haben
`439785` = Debuff wenn man von der Welle gehitted wird

## Infested Spawn
- Green Circles auf paar Spielern --> initial dmg + spawns adds mit random fixate
`455287` = Debuff wenn man von adds gefressen wird



"""


################################################################################
# Phases


boss.add_phase(name="Kick {phase}", spell_id=439795, event_type="begincast")
