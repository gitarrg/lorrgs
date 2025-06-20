import itertools
import json
import os
import sys

from lorgs.data.season import CURRENT_SEASON
from lorgs.models.raid_boss import RaidBoss

# data
from lorgs.data.classes import *
from lorgs.data.items import *
from lorgs.data.expansions.the_war_within.raids.undermine import *

import pandas as pd

from lorgs.models.warcraftlogs_ranking import SpecRanking


ALL_BOSSES: list[RaidBoss] = []
for raid in CURRENT_SEASON.raids:
    ALL_BOSSES.extend(raid.bosses)

METRICS = ["dps", "hps", "bossdps"]


################################################################################
# Get uses


def get_spec_ranking(
    spec: WowSpec,
    boss: RaidBoss,
    difficulty: str = "mythic",
    metric: str = "dps",
) -> SpecRanking:
    """Get the spec ranking for a given spec, boss, difficulty and metric."""
    key = f"spells/{spec.full_name_slug}__{boss.full_name_slug}__{difficulty}__{metric}.json"

    if os.path.exists(key):
        with open(key, "r") as f:

            try:
                spec_ranking = SpecRanking(**json.load(f))
            except json.JSONDecodeError:
                print("Error loading JSON:", key)
            else:
                return spec_ranking

    spec_ranking = SpecRanking.get_or_create(
        spec_slug=spec.full_name_slug,
        boss_slug=boss.full_name_slug,
        difficulty=difficulty,
        metric=metric,
    )
    with open(key, "w") as f:
        f.write(
            spec_ranking.model_dump_json(
                indent=2,
                by_alias=True,
                exclude_unset=True,
            )
        )
    return spec_ranking


def process_class(class_: WowClass) -> None:

    ############################################################################
    # Get Class

    # class_ = WowClass.get(name=class_name)
    # if not class_:
    #     print("Invalid class name:", class_name)
    #     return

    specs = class_.specs

    # Init the DataFrame
    spells: set[WowSpell] = set()

    for spec in specs:
        spells |= set(spec.all_spells + spec.all_buffs + spec.all_debuffs + spec.all_events)
        # for spell in spells:
        #     print(spell.spell_id, spell.name)

    df = pd.DataFrame(
        {
            "spell_id": [spell.spell_id for spell in spells],
            "name": [spell.name for spell in spells],
            "query": [spell.query for spell in spells],
            # "icon": [spell.icon for spell in spells],
            "uses": 0,
        }
    )
    df["query"] = df["query"].astype(bool)

    ###################################

    for spec, boss, metric in itertools.product(specs, ALL_BOSSES, METRICS):

        spec_ranking = get_spec_ranking(spec, boss, metric=metric)
        if not spec_ranking:
            print(f"SpecRanking not found for {spec.full_name} {boss.full_name_slug} {metric}")
            continue

        for report in spec_ranking.reports:
            for fight in report.fights:
                for player in fight.players:

                    for cast in player.casts:

                        if cast.spell_id not in df["spell_id"].values:

                            df.loc[len(df)] = {
                                "spell_id": cast.spell_id,
                                "name": "unknown",
                                "uses": 0,
                            }

                        df.loc[df["spell_id"] == cast.spell_id, "uses"] += 1
                        # print(spell.spell_id, spell.name, spell.uses)
    # break

    ###################################

    print(df)
    df.sort_values(by="uses", ascending=False, inplace=True)
    df.to_csv(f"spells/{class_.name_slug}.csv", index=False)


def load_data():
    for class_ in WowClass.list():
        if class_.id < 100:
            process_class(class_)


def combine_csvs():
    all_files = os.listdir("spells")
    all_files = [f for f in all_files if f.endswith(".csv")]

    df = pd.DataFrame()

    for file in all_files:
        print(file)
        df_ = pd.read_csv(f"spells/{file}")
        df = pd.concat([df, df_], ignore_index=True)

    df.sort_values(by="uses", ascending=False, inplace=True)
    df.to_csv("spells/all.csv", index=False)


combine_csvs()
