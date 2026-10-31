from datetime import datetime
import json

import cattrs
from lorgs.logger import Timer
from lorgs.models.warcraftlogs_ranking import SpecRanking


TEMP_FILE = "/mnt/d/tmp.json"


# converter = Converter()

cattrs.register_unstructure_hook(datetime, lambda dt: dt.isoformat())
cattrs.register_structure_hook(datetime, lambda iso, _: datetime.fromisoformat(iso))


def test(n, func, *args, **kwargs) -> None:

    times: list[float] = []
    for _ in range(n):
        with Timer(func.__name__) as t:
            func(*args, **kwargs)
        times.append(t.elapsed_time)

    total = sum(times)
    print(f"DONE | total={total:0.2f}s | avg: {1000 * total / n:0.4f}ms")


def structure(data) -> SpecRanking:
    return cattrs.structure(data, SpecRanking)


def parse(data) -> SpecRanking:
    return SpecRanking.parse_obj(data)


def load1() -> None:

    with Timer("read file"):
        with open(TEMP_FILE, "r") as f:
            data = json.load(f)

    """
    with Timer("parse_obj"):
        SpecRanking.parse_obj(data)

    with Timer("construct"):
        x = SpecRanking.construct(**data)
        # print(x)
    """

    n = 10

    # test(1_000, parse, data)
    for i in range(n):
        with Timer("parse"):
            SpecRanking.parse_obj(data)
        with Timer("construct"):
            SpecRanking.construct(**data)
    # for report in x.reports:
    #     print(report.start_time)
    # print(report.add_player)

    # test(50_000, structure, data)
    # with Timer("structure", i=50):
    #     x = structure(data)
    #     print(len(x.reports))
    #     return

    # print(data)


def main() -> None:
    load1()


if __name__ == "__main__":
    main()
