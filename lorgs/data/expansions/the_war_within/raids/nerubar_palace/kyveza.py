"""06: Ky'veza."""

from lorgs.models.raid_boss import RaidBoss


KYVEZA = RaidBoss(
    id=2920,
    name="Nexus-Princess Ky'veza",
    nick="Ky'veza",
    icon="inv_achievement_raidnerubian_etherealassasin.jpg",
)
boss = KYVEZA


# Portal Spawns
boss.add_cast(
    spell_id=436971,
    name="Assassination",
    duration=6,
    color="hsl(270, 60%, 60%)",
    icon="ability_theblackarrow.jpg",
)

# Portal Charge
boss.add_cast(
    spell_id=438245,
    name="Twilight Massacre",
    duration=6,
    color="hsl(300, 60%, 60%)",
    icon="ability_mage_netherwindpresence.jpg",
)


# Big AOE
boss.add_cast(
    spell_id=435405,
    name="Starless Night",
    duration=5 + 24,
    color="#bf4040",
    icon="spell_shadow_twilight.jpg",
    variations=[
        442277,  # 3rd AOE = Enrage "Eternal Night"
    ],
)


# Small AOEs
boss.add_cast(
    spell_id=437620,
    name="Nether Rift",
    duration=4 + 6,
    color="#d17a32",
    icon="spell_priest_void-blast.jpg",
)


# 440377 / Void Shredders = Tank Hit Initial DMG
# 440576 / Chasmal Gash = Tank Hit Dot (35sec)
boss.add_cast(
    spell_id=440377,
    name="Void Shredders",
    duration=35,  # duration of Chasmal Gash
    color="#478fb3",
    icon="ability_mount_voidelfstridermount.jpg",
    show=False,
)
