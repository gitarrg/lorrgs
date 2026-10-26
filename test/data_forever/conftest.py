"""Tests in here use Forever's real game data, so they only run with `LORRGS_GAME_VERSION=forever`."""

from test.helpers import require_game_version


require_game_version("forever")
