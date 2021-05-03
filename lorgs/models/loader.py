"""Some Functions to load and create Models.

This could probl be added to either the Models or the Client Class..
but in order to keep them a bit more organized..
I decided to move all this logic to its own place

"""

# IMPORT STANDARD LIBRARIES
import asyncio

# IMPORT THIRD PARTY LIBRARIES
import textwrap

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.client import WarcraftlogsClient
from lorgs.logger import logger
from lorgs.models.encounters import RaidZone
from lorgs.models.encounters import RaidBoss
# from lorgs.models.reports import Fight
from lorgs.models.reports import Report
from lorgs.models.specs import WowClass
from lorgs.models.specs import WowSpec
# from lorgs.models.specs import WowSpell
from lorgs.data import SPELLS


WCL_CLIENT = WarcraftlogsClient.get_instance()


################################################################################
#
#   CASTS
#
################################################################################


async def load_spell_icons(spells):
    logger.info("%d spells", len(spells))

    # Build query
    queries = [f"spell_{spell.spell_id}: ability(id: {spell.spell_id}) {{id, name, icon}}" for spell in spells]
    queries = "\n".join(queries)
    query = f"""
    gameData
    {{
        {queries}
    }}
    """
    data = await WCL_CLIENT.query(query)
    data = data.get("gameData", {})

    return data


@utils.as_list
def load_player_casts(player, casts_data):
    """Process the result of a casts-query to create Cast objects."""
    if not casts_data:
        logger.warning("casts_data is empty")
        return

    for cast_data in casts_data:
        if cast_data.get("sourceID") != player.source_id:
            continue

        # skip "begincast" events
        if cast_data.get("type") != "cast":
            continue

        cast = player.add_cast()
        cast.timestamp = cast_data["timestamp"]
        spell_id = cast_data["abilityGameID"]
        cast.spell_id = spell_id
        yield cast


################################################################################
#
#   PLAYERS
#
################################################################################

@utils.as_list
def load_fight_players(fight, players_data):
    if not players_data:
        logger.warning("players_data is empty")
        return

    total_damage = players_data.get("damageDone", [])
    total_healing = players_data.get("healingDone", [])

    # player_by_id = {}  # TODO: add to FightClass
    for composition_data in players_data.get("composition", []):

        spec_data = composition_data.get("specs", [])
        if not spec_data:
            logger.warning("Player has no spec: %s", composition_data.get("name"))
            continue

        spec_data = spec_data[0]
        spec_name = spec_data.get("spec")

        class_name = composition_data.get("type")
        class_names = {}
        class_names["DemonHunter"] = "Demon Hunter"
        class_names["DeathKnight"] = "Death Knight"
        class_name = class_names.get(class_name) or class_name

        wow_class = WowClass.get(name=class_name)
        if not wow_class:
            logger.warning("Unknown Class: %s", class_name)
            continue

        # spec = WowSpec.query
        # spec = spec.join(WowSpec.wow_class) # join the class so we can filter
        # spec = spec.filter(WowClass.name == class_name)
        # spec = spec.filter(WowSpec.name == spec_name)
        # spec = spec.first()

        spec_names = {}
        spec_names["BeastMastery"] = "Beast Mastery"
        spec_name = spec_names.get(spec_name) or spec_name

        spec = WowSpec.get(wow_class=wow_class, name=spec_name)
        if not spec:
            logger.warning("Unknown Spec: %s", spec_name)
            continue

        # Get Total Damage or Healing
        spec_role = spec_data.get("role")
        total_data = total_healing if spec_role == "healer" else total_damage
        for data in total_data:
            if data.get("id", -1) == composition_data.get("id"):
                total = data.get("total", 0) / (fight.duration / 1000)
                break
        else:
            total = 0

        # create and return yield player object
        player = fight.add_player()
        player.spec = spec
        player.name = composition_data.get("name")
        player.total = total
        player.source_id = composition_data.get("id")
        yield player


################################################################################
#
#   FIGHTS
#
################################################################################

def fight_data_query(fight, spells=None):
    """Construct the Query to fetch all info in a Fight.

    Args:
        fight(<Fight>): the fight we want to fetch
        spells[list(Spell)]: the spells we want to fetch (queries all spells if None)

    Returns:
        str: the constructed query string

    """

    def spell_ids(spells):
        spells = sorted(spell.spell_id for spell in spells)
        return ",".join(str(i) for i in spells)

    table_query_args = f"fightIDs: {fight.fight_id}, startTime: {fight.start_time}, endTime: {fight.end_time}"

    # Build Players Query (if needed)
    if fight.players:
        player_query = ""

        # Build Casts Filter
        casts_filters = [
            f"(source.name='{player.name}' and ability.id in ({spell_ids(player.spec.spells)}))"
            for player in fight.players
        ]
        casts_filter = " or ".join(casts_filters)

    else: # no player --> we need to fetch them
        player_query = f"players: table({table_query_args}, dataType: Summary)"
        casts_filter = f"ability.id in ({spell_ids(spells or SPELLS)})"

    logger.debug("player_query: %s", player_query)
    logger.debug("casts_filter: %s", casts_filter)

    casts_query = f"casts: events({table_query_args}, dataType: Casts, filterExpression: \"{casts_filter}\") {{data}}"
    return textwrap.dedent(f"""\
    reportData {{
        report(code: "{fight.report.report_id}") {{
            {player_query}
            {casts_query}
        }}
    }}
    """)


async def load_fights(fights):
    """Load a list of Fights.

    Args:
        fights[list(<Fight>)]

    """
    logger.debug("start loading %d fights", len(fights))
    queries = [fight_data_query(fight) for fight in fights]

    # Get Queries
    data = await WCL_CLIENT.multiquery(queries)

    # Process
    for fight, fight_data in zip(fights, data):
        report_data = fight_data.get("report") or {}
        players_data = report_data.get("players", {}).get("data", {})
        casts_data = report_data.get("casts", {}).get("data", [])

        if not fight.players: # only if they arn't loaded yet
            fight.players = load_fight_players(fight, players_data)

        for player in fight.players:
            player.casts = load_player_casts(player, casts_data)

    logger.debug("load_fights end")


################################################################################
#
#   REPORTS
#
################################################################################

async def load_report_info(report, fight_ids=None):
    """Fetch all fights in this report.

    Args:
        report(<Report>): the report

        fight_ids(list[int], optional): list of fights to load.
            loads all fights, if not specified.

    """
    query = f"""
    reportData
    {{
        report(code: "{report.report_id}")
        {{
            title
            zone {{name id}}
            startTime

            # masterData
            # {{
            #     actors(type: "Player")
            #     {{
            #         name
            #         id
            #     }}
            # }}

            fights(fightIDs: {fight_ids or []})
            {{
                id
                encounterID
                startTime
                endTime
                fightPercentage
                # kill
            }}
        }}
    }}
    """
    data = await WCL_CLIENT.query(query)
    report_data = data.get("reportData", {}).get("report", {})

    # Update the Report itself
    report.title = report_data.get("title", "")
    report.start_time = report_data.get("startTime", 0)

    zone_id = report_data.get("zone", {}).get("id")
    report.zone = RaidZone.get(id=zone_id)

    # Update the Fights in this report
    for fight_data in report_data.get("fights", []):

        boss_id = fight_data.get("encounterID")
        if not boss_id:
            continue

        # Get the fight
        fight = report.add_fight()
        fight.fight_id = fight_data.get("id")
        fight.start_time = fight_data.get("startTime", 0)
        fight.end_time = fight_data.get("endTime", 0)
        fight.boss = RaidBoss.get(id=boss_id)
        fight.percent = fight_data.get("fightPercentage")


async def load_report(report):
    """Load a single Report.

    Args:
        report(<Report>): the report to load.

    """
    logger.info(f"{report} | start")
    if not report.fights:
        logger.info(f"{report} | load info")
        await load_report_info(report)

    logger.info(f"{report} | load fights")
    fights_to_load = [fight for fight in report.fights if not fight.players]
    await load_fights(fights_to_load)
    return report


################################################################################
#
#   RANKINGS
#
################################################################################

async def load_char_rankings_source_ids(rankings):
    """Fetch and add the source_id's for ranking data."""
    queries = []
    for ranking_data in rankings:
        report_data = ranking_data.get("report", {})
        report_id = report_data.get("code")
        player_class = ranking_data.get("class")
        query = f"""\
            reportData
            {{
                report(code: "{report_id}")
                {{
                    masterData
                    {{
                        actors(type: "Player", subType: "{player_class}")
                        {{
                            name
                            id
                        }}
                    }}
                }}
            }}
            """
        queries.append(query)

    # run the queries
    data = await WCL_CLIENT.multiquery(queries)

    # process the data
    for ranking_data, report_data in zip(rankings, data):
        report_data = report_data.get("report") or {}
        master_data = report_data.get("masterData") or {}
        if not master_data:
            continue

        for actor in master_data.get("actors") or []:
            actor_name = actor.get("name")
            if actor_name == ranking_data["name"]:
                ranking_data["source_id"] = actor.get("id", -1)
                break


async def load_char_rankings(boss, spec, difficulty=5, limit=50):
    """Get Top Ranks for a given boss and spec."""
    logger.info(f"{boss.name} vs. {spec.name} {spec.wow_class.name} START")

    # Build and run the query
    query = f"""\
    worldData
    {{
        encounter(id: {boss.id})
        {{
            characterRankings(
                className: "{spec.wow_class.name_slug_cap}",
                specName: "{spec.name_slug_cap}",
                metric: {spec.role.metric},
                includeCombatantInfo: false,
                serverRegion: "EU",
            )
        }}
    }}
    """

    data = await WCL_CLIENT.query(query)
    data = data.get("worldData", {}).get("encounter", {}).get("characterRankings", {})

    rankings = data.get("rankings", [])
    if limit:
        rankings = rankings[:limit]

    logger.debug(f"{boss.name} vs. {spec.name} {spec.wow_class.name} load source ids")
    await load_char_rankings_source_ids(rankings)

    players = []
    for ranking_data in rankings:
        report_data = ranking_data.get("report", {})

        # skip hidden reports
        if ranking_data.get("hidden"):
            continue

        # Report
        report = Report(report_id=report_data.get("code"))

        # Fight
        fight = report.add_fight()
        fight.fight_id = report_data.get("fightID")
        fight.boss = boss
        fight.start_time = ranking_data.get("startTime", 0) - report_data.get("startTime", 0)
        fight.end_time = fight.start_time + ranking_data.get("duration", 0) # TODO: check property thing

        # Player
        player = fight.add_player()
        player.source_id = ranking_data.get("source_id")
        player.name = ranking_data.get("name")
        player.spec = spec
        player.total = ranking_data.get("amount", 0)

        # reports.append(report)
        players.append(player)

    logger.debug(f"{boss.name} vs. {spec.name} {spec.wow_class.name} load casts")

    fights = [player.fight for player in players]
    # load in chunks of 10 each
    for chunk in utils.chunks(fights, 10):
        await load_fights(chunk)

    # this should not really happen..
    players = [player for player in players if player.casts]
    return players
