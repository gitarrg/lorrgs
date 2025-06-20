import datetime
from lorgs.models.warcraftlogs_user_report import UserReport

import boto3
from boto3.dynamodb.conditions import Attr

# TYPES
from mypy_boto3_dynamodb.service_resource import Table


def find_reports(table: Table, LastEvaluatedKey=None):
    print(".")

    #  min_time = datetime.datetime.now() - datetime.timedelta(days=180)
    # expr = Attr("zone_id").gt(42)  # & Attr("guild").eq("Liquid")

    min_time = "2025-03-01T00:00:0.0"
    expr = Attr("updated").gt(min_time)
    expr = expr & Attr("guild").eq("Myth")

    kwargs = {}
    if LastEvaluatedKey:
        kwargs["ExclusiveStartKey"] = LastEvaluatedKey

    response = table.scan(
        FilterExpression=expr,
        ProjectionExpression="guild, report_id, zone_id, updated",
        Limit=50,
        # ExclusiveStartKey=LastEvaluatedKey or {},
        **kwargs
    )
    # print(response)

    for item in response.get("Items", []):
        print(item)

    if "LastEvaluatedKey" in response:
        find_reports(table, response["LastEvaluatedKey"])


def main() -> None:

    # import boto3
    # dynamodb = boto3.resource("dynamodb")

    table = UserReport.get_table()
    find_reports(table)


if __name__ == "__main__":
    main()
