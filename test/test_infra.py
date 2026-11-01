import pytest


def test_planner_runs_at_minute_one_of_every_hour():
    from infra.stacks import PLANNER_CRON

    assert PLANNER_CRON == "cron(1 * * * ? *)"


def test_builds_cron_is_daily():
    from infra.stacks import builds_cron

    assert builds_cron(0) == "cron(30 3 * * ? *)"
    assert builds_cron(2) == "cron(30 5 * * ? *)"
    with pytest.raises(ValueError):
        builds_cron(6)
