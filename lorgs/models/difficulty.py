import enum


class RaidDifficulty(enum.Enum):
    """Difficulty of the raid.
    
    IDs are matching the WCL IDs.
    """
    UNKNOWN = 0

    LFR = 1
    NORMAL = 3
    HEROIC = 4
    MYTHIC = 5
