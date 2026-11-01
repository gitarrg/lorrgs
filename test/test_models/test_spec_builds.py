from lorgs.models import spec_builds
from lorgs.models.spec_builds import TalentScope, assign_talents, find_builds


SPEC = list(range(1, 11))
HERO_A = [21, 22, 23]
HERO_B = [31, 32, 33]
CLASS = [101, 102]

SCOPE = TalentScope(
    counted=frozenset(SPEC + HERO_A + HERO_B),
    hero_trees={**{e: "tree-a" for e in HERO_A}, **{e: "tree-b" for e in HERO_B}},
)


def talents(*entries: int) -> dict[int, int]:
    return {entry: 1 for entry in entries}


def pool_of(*groups: tuple[int, dict[int, int]]) -> list[dict[int, int]]:
    return [t for count, t in groups for _ in range(count)]


def test_two_clear_groups():
    a = talents(1, 2, 3, 4, 5, *HERO_A)
    b = talents(6, 7, 8, 9, 10, *HERO_A)
    result = find_builds(pool_of((60, a), (40, b)), SCOPE)

    assert result.fights == 100
    assert result.other == 0
    assert result.settings.threshold == 0
    assert [build.letter for build in result.builds] == ["A", "B"]
    assert [build.fights for build in result.builds] == [60, 40]
    assert result.builds[0].talents == a
    assert result.builds[1].talents == b
    assert result.builds[0].hero_tree == "tree-a"
    # the other Build's talents are what sets a Build apart
    assert result.builds[0].defining.has == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
    assert result.builds[0].defining.lacks == {6: 1, 7: 1, 8: 1, 9: 1, 10: 1}


def test_single_build():
    a = talents(1, 2, 3, *HERO_A)
    result = find_builds(pool_of((96, a), (4, talents(1, 2, 4, *HERO_A))), SCOPE)

    assert len(result.builds) == 1
    assert result.builds[0].defining.has == {}
    assert result.builds[0].defining.lacks == {}


def test_small_hero_tree_group_above_min_share_is_a_build():
    main = talents(1, 2, 3, 4, *HERO_A)
    # same spec talents, other hero tree: a distance of 6 only because of the hero entries
    small = talents(1, 2, 3, 4, *HERO_B)
    noise = [talents(5, 6, 7, 8, 9, 10), talents(1), talents(2, 3, 4, 8)]  # too far apart to merge
    result = find_builds(pool_of((80, main), (12, small), *[(3, n) for n in noise]), SCOPE)

    assert [build.hero_tree for build in result.builds] == ["tree-a", "tree-b"]
    assert result.builds[1].fights == 12


def test_group_below_min_share_is_other():
    main = talents(1, 2, 3, *HERO_A)
    result = find_builds(pool_of((96, main), (4, talents(6, 7, 8, 9, *HERO_B))), SCOPE)

    assert len(result.builds) == 1
    assert result.other == 4


def test_hero_trees_never_share_a_build_even_when_merging():
    # many loadouts close enough to merge; the two hero trees differ by one entry, plus hero choice
    pool = []
    for i in range(10):
        pool += [talents(1, 2, 3, 4, 5, i + 1, *HERO_A)] * 6
        pool += [talents(1, 2, 3, 4, 5, i + 1, *HERO_B)] * 5
    result = find_builds(pool, SCOPE)

    for build in result.builds:
        trees = {SCOPE.hero_trees[e] for e in build.talents if e in SCOPE.hero_trees}
        assert len(trees) == 1
    assert {build.hero_tree for build in result.builds} == {"tree-a", "tree-b"}
    # a player in one hero tree is never assigned to the other's Build
    player = talents(1, 2, 3, 4, 5, 1, *HERO_B)
    assert assign_talents(player, result, SCOPE).hero_tree == "tree-b"


def test_class_talents_are_ignored_for_grouping_but_kept_in_the_loadout():
    a = talents(1, 2, 3, 101, *HERO_A)
    b = talents(1, 2, 3, 102, *HERO_A)
    result = find_builds(pool_of((30, a), (20, b)), SCOPE)

    assert len(result.builds) == 1
    assert result.builds[0].talents == a  # the most common full loadout
    assert result.builds[0].fights == 50


def test_ignore_list():
    a = talents(1, 2, 3, 4, *HERO_A)
    b = talents(1, 2, 3, 4, 5, 6, 7, 8, *HERO_A)

    assert len(find_builds(pool_of((30, a), (30, b)), SCOPE).builds) == 2
    result = find_builds(pool_of((30, a), (30, b)), SCOPE, ignore=[5, 6, 7, 8])
    assert len(result.builds) == 1
    assert result.settings.ignore == [5, 6, 7, 8]


def test_force_new_build_list():
    # one entry apart: grouped at threshold 1, unless the entry is forced
    a = talents(1, 2, 3, 4, *HERO_A)
    b = talents(1, 2, 3, 4, 5, *HERO_A)
    c = talents(1, 2, 3, 4, 6, *HERO_A)
    pool = pool_of((40, a), (30, b), (30, c))

    result = find_builds(pool, SCOPE, force_new_build=[5])
    assert result.settings.force_new_build == [5]
    with_5 = [build for build in result.builds if 5 in build.talents]
    without_5 = [build for build in result.builds if 5 not in build.talents]
    assert len(with_5) == 1
    assert len(without_5) >= 1
    assert all(5 not in build.talents for build in without_5)


def test_one_moved_point_is_not_other_at_threshold_zero():
    main = talents(1, 2, 3, 4, *HERO_A)
    moved = talents(1, 2, 3, 5, *HERO_A)  # distance 2
    result = find_builds(pool_of((96, main), (4, moved)), SCOPE)

    assert result.settings.threshold == 0
    assert len(result.builds) == 1
    assert result.other == 0
    assert result.builds[0].fights == 100


def test_ranks_count_as_a_difference():
    a = {1: 2, 2: 2, 3: 2, 4: 2, 21: 1}
    b = {1: 1, 2: 1, 3: 1, 4: 1, 21: 1}
    scope = TalentScope(frozenset({1, 2, 3, 4, 21}), {21: "tree-a"})
    assert len(find_builds(pool_of((50, a), (50, b)), scope).builds) == 2


def test_empty_pool():
    result = find_builds([], SCOPE)
    assert result.builds == []
    assert result.fights == 0


def test_assign_talents():
    a = talents(1, 2, 3, 4, 5, *HERO_A)
    b = talents(6, 7, 8, 9, 10, *HERO_A)
    result = find_builds(pool_of((60, a), (40, b)), SCOPE)

    assert assign_talents(a, result, SCOPE).letter == "A"
    assert assign_talents(talents(6, 7, 8, 9, 10, 101, *HERO_A), result, SCOPE).letter == "B"
    assert assign_talents(talents(1, 2, 8, 9, *HERO_A), result, SCOPE) is None  # 5 nodes from either


def test_max_builds():
    scope = TalentScope(frozenset(range(1, 51)), {})
    pool = []
    for i in range(10):
        pool += [talents(*range(5 * i + 1, 5 * i + 6))] * 10  # 10 nodes apart from each other
    result = find_builds(pool, scope)
    assert len(result.builds) <= spec_builds.MAX_BUILDS


def test_defining_talents_compare_within_the_hero_tree():
    a = talents(1, 2, 3, 4, *HERO_A)
    b = talents(1, 5, 6, 7, 8, *HERO_A)
    c = talents(6, 7, 8, 9, *HERO_B)  # alone on its hero tree: the tree stands in
    result = find_builds(pool_of((40, a), (35, b), (25, c)), SCOPE)

    by_tree = {build.hero_tree: build for build in result.builds if build.hero_tree == "tree-b"}
    assert by_tree["tree-b"].defining.has == {}
    assert by_tree["tree-b"].defining.lacks == {}
    build_a = next(build for build in result.builds if 4 in build.talents)
    assert build_a.defining.has == {2: 1, 3: 1, 4: 1}
    assert build_a.defining.lacks == {5: 1, 6: 1, 7: 1, 8: 1}


def test_distance_counts_nodes():
    scope = TalentScope(frozenset(range(1, 7)), {}, nodes={1: 100, 2: 100, 3: 101, 4: 102})

    def dist(a: dict[int, int], b: dict[int, int]) -> int | None:
        return spec_builds.distance(*(spec_builds._project(t, scope, (), ()) for t in (a, b)))

    assert dist(talents(1, 5), talents(2, 5)) == 1  # a choice node swapped
    assert dist({3: 1}, {3: 2}) == 1  # a rank
    assert dist(talents(3, 5), talents(4, 5)) == 2  # a point moved to another node


def test_builds_within_merge_distance_are_one():
    main = talents(1, 2, 3, 4, *HERO_A)
    variant = talents(1, 2, 5, 6, *HERO_A)  # 4 entries, but the same 4 nodes when 3/5 and 4/6 are choices
    far = talents(7, 8, 9, 10, *HERO_A)
    scope = TalentScope(SCOPE.counted, SCOPE.hero_trees, nodes={3: 200, 5: 200, 4: 201, 6: 201})

    assert len(find_builds(pool_of((50, main), (30, variant), (20, far)), SCOPE).builds) == 3
    result = find_builds(pool_of((50, main), (30, variant), (20, far)), scope)
    assert [build.fights for build in result.builds] == [80, 20]
    assert result.builds[0].talents == main


def test_assign_reach():
    main = talents(1, 2, 3, 4, *HERO_A)
    result = find_builds(pool_of((100, main)), SCOPE)

    assert result.settings.assign_reach == spec_builds.ASSIGN_REACH == 4
    assert assign_talents(talents(1, 2, 5, 6, *HERO_A), result, SCOPE).letter == "A"  # 4 nodes
    assert assign_talents(talents(1, 5, 6, 7, *HERO_A), result, SCOPE) is None  # 5 nodes
