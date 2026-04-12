"""Some Basic Deyugging Routes."""
# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.clients import sqs


router = fastapi.APIRouter(tags=["debug"])


@router.get("/ping")
def ping():
    """Basic Ping to check Server Status."""
    return {"reply": "Hi!", "time": datetime.datetime.now(datetime.timezone.utc).isoformat()}


@router.get("/ping/no_cache")
def ping_no_cache(response: fastapi.Response):
    """Basic Ping without Caching."""
    response.headers["Cache-Control"] = "no-cache"
    return {"reply": "Hi! No Cache", "time": datetime.datetime.now(datetime.timezone.utc).isoformat()}


@router.get("/ping/discord")
def ping_dc(response: fastapi.Response):
    """Basic Ping sendng a message via sqs to discord."""
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    payload = {"Text": "Hello", "time": ts}

    
    message = sqs.send_message(payload)
    payload["id"] = message["MessageId"]

    response.headers["Cache-Control"] = "no-cache"
    return payload
