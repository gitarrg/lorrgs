"""Tests in here use Retail's real game data, so they only run with `LORRGS_GAME_VERSION=retail`."""

from test.helpers import require_game_version


require_game_version("retail")
