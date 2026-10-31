import json
import boto3
import time
import typing


G: dict[str, typing.Any] = {"invocations": 0}


class Timer:
    def __init__(self, name: str):
        self.name = name
        self.start_time: float = time.time()

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.start_time

    @property
    def elapsed_time_ms(self) -> float:
        return round(self.elapsed_time * 1000, ndigits=2)

    def print(self) -> None:
        print(f"{self.name}: {self.elapsed_time_ms:.02f}ms")

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, type, value, traceback):
        G[self.name] = f"{self.elapsed_time * 1000:.02f}ms"
        self.print()


s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

with Timer("get table"):
    table = dynamodb.Table("user")


def load_s3(bucket="lorrgs", key="dev/speed_test.json") -> str:

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"]
    return body.read().decode("utf-8")


def load_dynamo(key: str):
    response = table.get_item(
        Key={"id": key},
        ConsistentRead=False,
    )
    return response["Item"]


def lambda_handler(event=None, context=None) -> dict[str, typing.Any]:

    G["invocations"] += 1

    with Timer("s3"):
        load_s3()

    with Timer("dyn 1"):
        load_dynamo("123")

    with Timer("dyn 2"):
        load_dynamo("123")

    print(G)
    return {"statusCode": 200, "body": json.dumps(G)}


################################################################################

from datetime import datetime
import aiohttp
import asyncio
import itertools
import sys


async def run(url: str) -> None:

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

    items = [datetime.now().isoformat()]
    items += list(itertools.chain.from_iterable(data.items()))
    items = [str(item) for item in items]
    # items = "\t".join(f"{k}\t{v}" for k, v in )
    print(items)

    with open("/mnt/d/aws_speed_compare.log", "a") as f:
        f.write("\t".join(items) + "\n")


def main() -> None:
    url = sys.argv[1]
    asyncio.run(run(url))


if __name__ == "__main__":
    # main()
    lambda_handler()
