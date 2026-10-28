"""CDK app for the Game Versions deployed with CDK. Retail still uses `scripts/deploy.py`.

    scripts/deploy diff
    scripts/deploy
"""
from __future__ import annotations

# IMPORT THIRD-PARTY LIBRARIES
import aws_cdk as cdk
import dotenv

# IMPORT LOCAL LIBRARIES
from lorgs.game_version import FOREVER, MISTS

from .stacks import GameVersionStack, SharedStack


ENV = cdk.Environment(account="746912274922", region="eu-west-1")

# Game Version -> whether the 6h ranking refresh is on
GAME_VERSIONS = {
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

for game_version in GAME_VERSIONS:
    GameVersionStack(
        app,
        f"lorrgs-{game_version.name}",
        env=ENV,
        game_version=game_version,
        layers=shared.layers,
        schedule_enabled=False,
    )
app.synth()
