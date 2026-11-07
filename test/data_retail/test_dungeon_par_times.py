from lorgs.data import RETAIL


def test_current_dungeons_have_a_par_time():
    for dungeon in RETAIL.data.dungeons:
        assert dungeon.par_time > 0, dungeon.name
