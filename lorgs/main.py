# -*- coding: utf-8 -*-

# IMPORT STANDARD LIBRARIES
import asyncio
import os

# IMPORT THIRD PARTY LIBRARIES
import aiofiles
import jinja2
import dotenv

# IMPORT LOCAL LIBRARIES
from lorgs import client
from lorgs import models
from lorgs import utils
from lorgs import wow_data
from lorgs.logger import logger


dotenv.load_dotenv()


WCL_CLIENT_ID = os.getenv("WCL_CLIENT_ID")
WCL_CLIENT_SECRET = os.getenv("WCL_CLIENT_SECRET")


GOOGLE_ANALYTICS_ID = "G-Y92VPCY6QW"


PWD = os.path.dirname(__file__)

TEMPLATE_FOLDER = os.path.join(PWD, "templates")
TEMPLATE_LOADER = jinja2.FileSystemLoader(searchpath=TEMPLATE_FOLDER)
TEMPLATE_ENV = jinja2.Environment(loader=TEMPLATE_LOADER)
TEMPLATE_ENV.trim_blocks = True
TEMPLATE_ENV.lstrip_blocks = True

TEMPLATE_ENV.filters["format_time"] = utils.format_time
TEMPLATE_ENV.filters["format_big_number"] = utils.format_big_number
TEMPLATE_ENV.filters["slug"] = utils.slug

# str: folder where the generated html files will be saved
OUTPUT_FOLDER = os.path.join(PWD, "../_build")

DEBUG = os.getenv("DEBUG")


WCL_CLIENT = client.WarcraftlogsClient(client_id=WCL_CLIENT_ID, client_secret=WCL_CLIENT_SECRET)

################################################################################
#   Jinja
#

async def render(template_name, path, data=None):
    # print("[RENDER]", path)

    # include some global args
    data = data or {}
    data["wow_data"] = wow_data
    data["GOOGLE_ANALYTICS_ID"] = GOOGLE_ANALYTICS_ID

    # 250ms = 1px
    data["TIMESCALE"] = 250

    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        logger.info("creating folder: %s", dirpath)
        os.makedirs(dirpath)

    template = TEMPLATE_ENV.get_template(template_name)

    html = template.render(**data)
    async with aiofiles.open(path, 'w', encoding="utf-8") as f:
        await f.write(html)


async def render_index():
    data = {}
    # we need smth to make the links work
    data["spec"] = wow_data.WARLOCK_AFFLICTION
    data["boss"] = wow_data.ENCOUNTERS[-1]

    path = f"{OUTPUT_FOLDER}/index.html"
    await render("index.html", path, data)


async def render_spell_db():
    path = f"{OUTPUT_FOLDER}/spell_db.js"
    await render("elements/spell_db.js", path)


################################
#       Rankings
#

async def generate_ranking_report(boss, spec):

    fights = []
    fights = await WCL_CLIENT.get_top_ranks(boss["id"], spec)
    fights = fights[:50] # limit a bit for now
    if DEBUG:
        fights = fights[:20]

    await WCL_CLIENT.fetch_multiple_fights(fights)

    data = {}
    data["boss"] = boss
    data["spec"] = spec
    data["fights"] = fights

    # get a list of all used spells
    used_spells = [p.spells_used for f in fights for p in f.players]
    used_spells = utils.flatten(used_spells)
    used_spells = list(set(used_spells))
    data["all_spells"] = used_spells
    # data["all_spells"] = spec.spells.values()

    longest_fight = sorted(fights, key=lambda f: f.duration)[-1]
    data["timeline_duration"] = longest_fight.duration

    path = f"{OUTPUT_FOLDER}/rankings_{spec.full_name_slug}_{boss['name_slug']}.html"
    await render("ranking.html", path, data)

    logger.info(f"[GENERATED REPORT] {spec.full_name} vs {boss['name']}")
    return


async def generate_rankings():
    bosses = wow_data.ENCOUNTERS
    specs = wow_data.SPECS_SUPPORTED

    if DEBUG:
        bosses = [wow_data.ENCOUNTERS[-1]]
        specs = [
            # healers
            wow_data.DRUID_RESTORATION,
            # wow_data.PALADIN_HOLY,
            # wow_data.PRIEST_DISCIPLINE,
            # wow_data.PRIEST_HOLY,
            # wow_data.SHAMAN_RESTORATION,

            # mps
            # wow_data.PALADIN_RETRIBUTION,
            # wow_data.DEATHKNIGHT_UNHOLY,
            # wow_data.DEMONHUNTER_HAVOC,
            # wow_data.SHAMAN_ENHANCEMENT,

            # rdps
            # wow_data.SHAMAN_ELEMENTAL,
            # wow_data.WARRIOR_FURY,
            # wow_data.MONK_WINDWALKER,
            # wow_data.HUNTER_BEASTMASTERY,
            # wow_data.HUNTER_MARKSMANSHIP,
            # wow_data.MAGE_FIRE,
            # wow_data.WARLOCK_AFFLICTION,
            # wow_data.WARLOCK_DESTRUCTION,
        ]

    # tasks = []
    for spec in specs:
        # for boss in bosses:
        #     await generate_ranking_report(boss, spec)
        tasks = [generate_ranking_report(boss, spec) for boss in bosses]
        await asyncio.gather(*tasks)


    # await asyncio.gather(*tasks)
    # if DEBUG:
    #     n = 1
    #     tasks, tasks_cancel = tasks[:n], tasks[n:]
    #     for task in tasks_cancel:
    #         task.cancel()
    # await asyncio.gather(*tasks)


async def _generate_reports_index(heal_comps):
    data = {}
    data["boss"] = wow_data.ENCOUNTERS[-1] # Sire
    data["heal_comps"] = heal_comps
    path = f"{OUTPUT_FOLDER}/reports_index.html"
    await render("reports_index.html", path, data)


################################
#       Comps
#


async def _generate_comp_report(comp):
    boss = wow_data.ENCOUNTERS[-1] # Sire

    search = comp.get("search")
    logger.info("[COMP REPORT] find reports: %s", comp.get("name"))
    fights = await WCL_CLIENT.find_reports(encounter=boss["id"], search=search)

    if DEBUG:
        fights = fights[:5]

    # Get Spells and avoid duplicates
    spells = {spell_id: spell for spec in comp.get("specs") for spell_id, spell in spec.all_spells.items()}
    spells = spells.values()
    extra_filter = comp.get("extra_filter")

    await WCL_CLIENT.fetch_multiple_fights(fights, spells=spells, extra_filter=extra_filter)
    for fight in fights:
        fight.players.sort(key=lambda p: p.spec.full_name)

    # get a list of all used spells
    used_spells = [p.spells_used for f in fights for p in f.players]
    used_spells = utils.flatten(used_spells)
    used_spells = list(set(used_spells))

    # assemble data and render
    data = {}
    data["comp"] = comp
    data["boss"] = boss
    data["fights"] = fights
    data["all_spells"] = used_spells
    path = f"{OUTPUT_FOLDER}/comps_heal_{comp['name'].lower()}.html"
    await render("report.html", path, data)


async def generate_reports():
    await _generate_reports_index(wow_data.HEAL_COMPS)
    for comp in wow_data.HEAL_COMPS:
        await _generate_comp_report(comp)
        if DEBUG:
            return


async def generate_report_breakdown():

    report_id = "fHyWYVvpd4Lbn1wQ"


    report = models.Report(report_id=report_id)
    fights = await report.fetch_fights(WCL_CLIENT)

    # Get Spells and avoid duplicates
    # spells = wow_data.SPELLS.values()
    spells = utils.flatten([spec.spells.values() for spec in wow_data.HEALS])

    await WCL_CLIENT.fetch_multiple_fights(fights, spells=spells, extra_filter="")
    for fight in fights:
        fight.players = [p for p in fight.players if p.spec in wow_data.HEALS]
        fight.players.sort(key=lambda p: p.spec.full_name)


    # get a list of all used spells
    used_spells = [p.spells_used for f in fights for p in f.players]
    used_spells = utils.flatten(used_spells)
    used_spells = list(set(used_spells))

    # assemble data and render
    data = {}
    data["comp"] = wow_data.HEAL_COMPS[0]  # FIXME
    data["boss"] = wow_data.ENCOUNTERS[-1]  # FIXME: Get from report
    data["fights"] = fights
    data["all_spells"] = used_spells
    path = f"{OUTPUT_FOLDER}/report_breakdown_{report_id}.html"
    await render("report.html", path, data)



################################
#       Main
#

async def main():
    try:
        logger.info("starting")
        # load cache
        await WCL_CLIENT.cache.load()
        logger.info("loaded cache")

        # auth once
        if not DEBUG:
            await WCL_CLIENT.update_auth_token()
        logger.info("updated auth")

        await WCL_CLIENT.load_spell_icons(wow_data.ALL_SPELLS)
        await render_spell_db()

        # generate
        await render_index()
        await generate_reports()
        await generate_rankings()
        logger.info("generated rankings")
        # await generate_report_breakdown()

    except KeyboardInterrupt:
        logger.info("closing...")

    finally:
        if not DEBUG:
            logger.info("SAVING Cache!")
            await WCL_CLIENT.cache.save()


if __name__ == '__main__':
    asyncio.run(main())
