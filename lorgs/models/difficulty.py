from __future__ import annotations

from lorgs.utils import CaseInsensitiveEnum


class RaidDifficulty(CaseInsensitiveEnum):
    """Difficulty of the raid.
    
    IDs are matching the WCL IDs.
    """
    UNKNOWN = 0

    LFR = 1
    NORMAL = 3
    HEROIC = 4
    MYTHIC = 5
