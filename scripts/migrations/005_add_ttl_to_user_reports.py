# IMPORT STANDARD LIBRARIES
import datetime

# IMPORT THIRD PARTY LIBRARIES
from boto3.dynamodb.conditions import Attr

# IMPORT LOCAL LIBRARIES
from lorgs.models.warcraftlogs_user_report import UserReport

# TYPES
from mypy_boto3_dynamodb.service_resource import Table


def compute_ttl(iso_time: str) -> int:
    print("iso_time", type(iso_time), iso_time)
    dt = datetime.datetime.fromisoformat(iso_time.rstrip("Z"))  # Remove 'Z' if present
    ttl = dt + datetime.timedelta(days=365)
    return int(ttl.timestamp())  # Convert to Unix timestamp


def add_ttl(table: Table) -> None:
    """Scan the table and update items with missing TTL values."""
    expr = Attr("ttl").not_exists()
    last_evaluated_key = None

    while True:
        kwargs = {
            "FilterExpression": expr,
            # "ProjectionExpression": "updated",
            "Limit": 25,  # DynamoDB batch writes are limited to 25 items per request
        }
        if last_evaluated_key:
            kwargs["ExclusiveStartKey"] = last_evaluated_key

        response = table.scan(**kwargs)
        items = response.get("Items", [])

        # Prepare batch write requests in chunks of 25
        with table.batch_writer() as batch:
            for item in items:
                if "updated" in item:
                    ttl_value = compute_ttl(item["updated"])
                    if ttl_value > 0:
                        item["ttl"] = ttl_value
                        batch.put_item(Item=item)

        print(f"Updated {len(items)} items with TTL")

        last_evaluated_key = response.get("LastEvaluatedKey")
        if not last_evaluated_key:
            break  # Exit loop when there's no more data to scan


table = UserReport.get_table()
add_ttl(table)
