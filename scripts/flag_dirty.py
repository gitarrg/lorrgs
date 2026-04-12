#!/usr/bin/env python

import itertools

from lorgs.models.warcraftlogs_ranking import SpecRanking

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs
from lorgs.data.classes import *

from lorgs.data.expansions.midnight import *
from lorgs.data.expansions.midnight.raids.voidspire import *



def load_spec_rankings() -> None:
    bosses = [
        # *VOIDSPIRE.bosses,
        CROWN_OF_THE_COSMOS,
        *DREAMRIFT.bosses,
        *MARCH_ON_QUALDANAS.bosses,
    ]

    specs = [
        # DRUID_BALANCE,
        # SHAMAN_ELEMENTAL,
        # SHAMAN_RESTORATION,
        # MONK_MISTWEAVER,
        # MONK_WINDWALKER,
        # MONK_BREWMASTER,
        # ROGUE_ASSASSINATION,
        # ROGUE_OUTLAW,
        # ROGUE_SUBTLETY,
        # WARLOCK_DESTRUCTION,
        # WARLOCK_AFFLICTION,
        # WARLOCK_DEMONOLOGY,
        # HUNTER_BEASTMASTERY,
        # HUNTER_MARKSMANSHIP,
        # HUNTER_SURVIVAL,
        # MAGE_ARCANE,
        # MAGE_FIRE,
        # MAGE_FROST,
        # EVOKER_AUGMENTATION,
        # EVOKER_PRESERVATION,
        # DEMONHUNTER_HAVOC,
        # PRIEST_SHADOW,
        # SHAMAN_RESTORATION,
        # SHAMAN_ELEMENTAL,
        # SHAMAN_ENHANCEMENT
        # PRIEST_HOLY
        # MAGE_ARCANE,
        # PALADIN_HOLY,
        # MONK_WINDWALKER,
        # *MDPS.specs,
        # *RDPS.specs,
    ]
    specs = ALL_SPECS
    # specs = DPS.specs
    metrics = ["dps", "hps"]
    difficulties = ["heroic", "mythic"]

    for [spec, boss, difficulty, metric] in itertools.product(specs, bosses, difficulties, metrics):
        print(spec.full_name_slug, boss.full_name_slug, difficulty, metric)

        spec_ranking = SpecRanking.get_or_create(
            spec_slug=spec.full_name_slug,
            boss_slug=boss.full_name_slug,
            difficulty=difficulty,
            metric=metric,
        )
        if spec_ranking:
            spec_ranking.dirty = True
            spec_ranking.save()


if __name__ == "__main__":
    load_spec_rankings()
    # load_comp_ranking()
