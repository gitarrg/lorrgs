# IMPORT LOCAL LIBRARIES
from lorgs.data.retail.classes import *
from lorgs.models.dungeon import Dungeon
from lorgs.models.wow_trinket import WowTrinket


################################################################################
# Trinkets


GRIM_CODEX = WowTrinket(
    spell_id=345739,
    name="Grim Codex",
    icon="inv_misc_book_01.jpg",
    cooldown=90,
    item=178811,
)
"""On-Use Damage

> Use: Conjure a Spectral Scythe, dealing 861 Shadow damage to your target and
> 120 Shadow damage in a 15 yd cone to enemies behind your target. (1 Min, 30 Sec Cooldown)
"""

SOULLETTING_RUBY = WowTrinket(
    spell_id=345801,
    name="Soulletting Ruby",
    icon="inv_jewelcrafting_livingruby_01.jpg",
    duration=16,
    cooldown=120,
    item=178811,
)
"""On-Use crit

Cast: 345801
Buff: 345805

> Use: Draw out a piece of the target's soul, decreasing their movement speed by 30% until
> the soul reaches you. The soul instantly heals you for 398, and grants you up
> to 142 Critical Strike for 16 sec. You gain more Critical Strike from lower health targets. (2 Min Cooldown)
"""
SOULLETTING_RUBY.add_specs(*INT_SPECS)


# [Vial of Spectral Essence]
"""

spell_id=345695

> Use: Bind a spectral essence to an enemy for 20 sec, causing allied attacks
> to heal for 30% of damage dealt, up to 1345 total healing.
> When the essence expires or is removed early, the remaining healing bursts,
> healing up to 5 allies within 8 yds. (1 Min, 30 Sec Cooldown)
"""


# [Viscera of Coalesced Hatred]
"""
https://www.wowhead.com/item=178808/viscera-of-coalesced-hatred

> Equip: Your abilities have a very high chance to lash out with a Hateful Strike,
> dealing 158 Physical damage to an enemy and healing you for 7.
> These effects are increased by 100% while you are below 35% health.
"""


################################################################################


THEATER_OF_PAIN = Dungeon(
    name="Theater of Pain",
    trinkets=[
        SOULLETTING_RUBY,
    ],
)
