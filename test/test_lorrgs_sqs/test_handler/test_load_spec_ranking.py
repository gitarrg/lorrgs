import asyncio
import json
import typing

import dotenv

dotenv.load_dotenv()


from lorrgs_sqs.handler import load_spec_rankings


def build_test_message(**kwargs: typing.Any) -> dict[str, str]:
    return {"body": json.dumps(kwargs)}


async def run() -> None:

    # Inputs
    message = build_test_message(boss_slug="lords-of-dread", spec_slug="paladin-holy", limit=10)
    await load_spec_rankings.main(message=message)


async def main():
    await run()


if __name__ == "__main__":
    asyncio.run(main())
