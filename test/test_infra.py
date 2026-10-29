import pytest

from infra.stacks import refresh_cron


@pytest.mark.parametrize(
    ("offset", "expected"),
    [
        (0, "cron(0 0,6,12,18 * * ? *)"),  # Retail
        (1, "cron(0 1,7,13,19 * * ? *)"),  # Mists
        (2, "cron(0 2,8,14,20 * * ? *)"),  # Forever
    ],
)
def test_refresh_cron_offsets(offset, expected):
    assert refresh_cron(offset) == expected


def test_refresh_cron_rejects_offset_outside_interval():
    with pytest.raises(ValueError):
        refresh_cron(6)
