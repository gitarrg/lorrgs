# IMPORT THIRD PARTY LIBRARIES
from pydantic import BaseModel, model_validator

# IMPORT LOCAL LIBRARIES
from .report_data import Report
from .world_data import WorldData


class Query(BaseModel):
    """Root Query Object.

    ref: https://www.warcraftlogs.com/v2-api-docs/warcraft/query.doc.html
    """

    # characterData: CharacterData
    # Obtain the character data object that allows the retrieval of individual characters or filtered collections of characters.

    # gameData: GameData
    # Obtain the game data object that holds collections of static data such as abilities, achievements, classes, items, NPCs, etc..

    # guildData: GuildData
    # Obtain the guild data object that allows the retrieval of individual guilds or filtered collections of guilds.

    # progressRaceData: ProgressRaceData
    # Obtain information about an ongoing world first or realm first race. Inactive when no race is occurring. This data only updates once every 30 seconds, so you do not need to fetch this information more often than that.

    # rateLimitData: RateLimitData
    # Obtain the rate limit data object to see how many points have been spent by this key.

    report: Report | None = None

    # reportData: typing.Optional[ReportData]
    # """Obtain the report data object that allows the retrieval of individual reports
    # or filtered collections of reports by guild or by user."""

    # userData: UserData
    # Obtain the user object that allows the retrieval of the authorized user's id and username.

    worldData: WorldData | None = None
    """The world data object contains collections of data such as
    expansions, zones, encounters, regions, subregions, etc."""

    @model_validator(mode="before")
    @classmethod
    def unwrap_data(cls, v):
        return v.get("data", v)
