"""CDK app: `lorrgs-all` serves every Game Version; the old per-version stacks stay up until the cutover.

scripts/deploy diff
scripts/deploy
"""

from __future__ import annotations

# IMPORT THIRD-PARTY LIBRARIES
import aws_cdk as cdk
import dotenv

# IMPORT LOCAL LIBRARIES
from lorgs.data import FOREVER, MISTS, RETAIL

from .stacks import AllGameVersionsStack, GameVersionStack, RefreshSchedule, SharedStack


ENV = cdk.Environment(account="746912274922", region="eu-west-1")

# Game Version -> its 6h ranking refresh: offset by one hour each (Retail 0/6/12/18, Mists 1/7/13/19,
# Forever 2/8/14/20) to spread the Warcraft Logs quota. Enable one once it has boss data.
SCHEDULES = {
    RETAIL.name: RefreshSchedule(hour_offset=0, enabled=False),
    MISTS.name: RefreshSchedule(hour_offset=1, enabled=False),
    FOREVER.name: RefreshSchedule(hour_offset=2, enabled=False),
}

# Game Versions that still have an old per-version stack (Retail never had one)
OLD_GAME_VERSIONS = {
    MISTS,
    FOREVER,
}

dotenv.load_dotenv()  # the Lambdas' SECRETS (see infra/stacks.py)

app = cdk.App()

shared = SharedStack(
    app,
    "lorrgs-shared",
    env=ENV,
)

AllGameVersionsStack(
    app,
    "lorrgs-all",
    env=ENV,
    layers=shared.layers,  # ty: ignore[invalid-argument-type]
    schedules=SCHEDULES,
)

for game_version in OLD_GAME_VERSIONS:
    GameVersionStack(
        app,
        f"lorrgs-{game_version.name}",
        env=ENV,
        game_version=game_version,
        layers=shared.layers,  # ty: ignore[invalid-argument-type]
        schedule_enabled=False,
    )
app.synth()
