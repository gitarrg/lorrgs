"""CDK app: `lorrgs` (serves every Game Version; Lambda layers live in that stack).

scripts/deploy diff
scripts/deploy
"""

from __future__ import annotations

# IMPORT THIRD-PARTY LIBRARIES
import aws_cdk as cdk
import dotenv

# IMPORT LOCAL LIBRARIES
from lorgs.data import FOREVER, MISTS, RETAIL

from .stacks import LorrgsStack, RefreshSchedule


ENV = cdk.Environment(account="746912274922", region="eu-west-1")

# Game Version -> its 6h ranking refresh: offset by one hour each (Retail 0/6/12/18, Mists 1/7/13/19,
# Forever 2/8/14/20) to spread the Warcraft Logs quota. Enable one once it has boss data.
SCHEDULES = {
    RETAIL.name: RefreshSchedule(hour_offset=0, enabled=True, builds_enabled=True),
    MISTS.name: RefreshSchedule(hour_offset=1, enabled=False),
    FOREVER.name: RefreshSchedule(hour_offset=2, enabled=False),
}

dotenv.load_dotenv()  # the Lambdas' SECRETS and API_CERTIFICATE_ARN (see infra/stacks.py)

app = cdk.App()

LorrgsStack(
    app,
    "lorrgs",
    env=ENV,
    schedules=SCHEDULES,
)
app.synth()
