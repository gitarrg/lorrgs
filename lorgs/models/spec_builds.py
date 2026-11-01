"""Builds of a spec: groups of Talents that differ by only a few choices (see `GLOSSARY.md`).

`find_builds` is a pure function over the Talents of many Fights. `SpecBuilds` stores its result per spec and season.
The settings used are stored along, so the frontend assigns players to Builds by the same rules (`assign_talents`).
"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import collections
import dataclasses
import datetime
import string
import typing

# IMPORT THIRD PARTY LIBRARIES
import pydantic

# IMPORT LOCAL LIBRARIES
from lorgs.data import get_game_version
from lorgs.models.base import UTC_MIN, UTCDatetime
from lorgs.models.base.s3 import S3Model


if typing.TYPE_CHECKING:
    from collections.abc import Collection, Iterable, Mapping, Sequence


START_THRESHOLD = 0
"""Distance within which Talents are grouped, to begin with."""
CAP_THRESHOLD = 10
"""The threshold is never raised above this."""
COVER = 0.75
"""The threshold is raised until the Builds cover this share of the pool."""
MIN_SHARE = 0.05
"""A group needs this share of the pool to be a Build."""
MAX_BUILDS = 4
"""At most this many Builds per spec."""
MIN_ASSIGN = 2
"""A player is assigned to a Build within at least this distance, so that a single point moved to another talent
(distance 2: one entry loses its rank, one gains it) does not make a player "Other" when the threshold stays at 0."""


@dataclasses.dataclass(frozen=True)
class TalentScope:
    """Which talent entries of a spec count."""

    counted: frozenset[int]
    """Entries counting towards the distance: hero and spec talents. Class talents are left out."""

    hero_trees: Mapping[int, str]
    """Entry id -> slug of its hero tree, for the entries of a hero tree."""


@dataclasses.dataclass(frozen=True)
class _Point:
    """The Talents of one player, reduced to what the distance looks at."""

    ranks: frozenset[tuple[int, int]]
    """`(entry id, rank)` of the counted entries, without the ignored ones."""

    group: tuple[frozenset[str], frozenset[int]]
    """Hero trees and forced entries the player has. Points of different groups are never in the same Build."""


def _project(talents: Mapping[int, int], scope: TalentScope, ignore: Collection[int], force: Collection[int]) -> _Point:
    taken = {entry for entry, rank in talents.items() if rank > 0}
    return _Point(
        ranks=frozenset(
            (entry, rank)
            for entry, rank in talents.items()
            if rank > 0 and entry in scope.counted and entry not in ignore
        ),
        group=(
            frozenset(scope.hero_trees[entry] for entry in taken if entry in scope.hero_trees),
            frozenset(entry for entry in taken if entry in force),
        ),
    )


def distance(a: _Point, b: _Point) -> int | None:
    """Number of talent entries whose rank differs. `None` when the two can not be in one Build."""
    if a.group != b.group:
        return None
    return len({entry for entry, _ in a.ranks ^ b.ranks})


class BuildSettings(pydantic.BaseModel):
    """What the Builds were worked out with."""

    threshold: int
    min_assign: int = MIN_ASSIGN
    ignore: list[int] = []
    force_new_build: list[int] = []


class DefiningTalents(pydantic.BaseModel):
    """What sets a Build apart from the others, within the counted (hero and spec) talents. Entry id -> rank."""

    has: dict[int, int] = {}
    """Talents of this Build that no other Build has."""
    lacks: dict[int, int] = {}
    """Talents that every other Build has and this one lacks."""


class Build(pydantic.BaseModel):
    letter: str
    """A, B, ... by share."""

    fights: int
    """Fights (players) assigned to this Build."""

    hero_tree: str | None = None
    """Slug of the Build's hero tree."""

    talents: dict[int, int]
    """Main loadout: the most common full Talents among the members that have the Build's counted talents."""

    defining: DefiningTalents = DefiningTalents()


class BuildsResult(pydantic.BaseModel):
    fights: int = 0
    """Size of the pool: all Fights (players) with Talents."""

    other: int = 0
    """Fights not assigned to any Build."""

    settings: BuildSettings
    builds: list[Build] = []


@dataclasses.dataclass
class _Group:
    centre: _Point
    count: int
    members: list[_Point]


def _groups(counts: Mapping[_Point, int], threshold: int) -> list[_Group]:
    """Greedy: the most common remaining Talents become a centre and claim all the remaining ones within `threshold`."""
    remaining = sorted(counts, key=lambda point: -counts[point])  # stable: ties keep their first-seen order
    groups = []
    while remaining:
        centre = remaining[0]
        members = [p for p in remaining if (dist := distance(centre, p)) is not None and dist <= threshold]
        groups.append(_Group(centre, sum(counts[p] for p in members), members))
        claimed = set(members)
        remaining = [p for p in remaining if p not in claimed]
    return groups


def _letter(index: int) -> str:
    return string.ascii_uppercase[index]


def _assign(point: _Point, centres: Sequence[_Point], reach: int) -> int | None:
    """Index of the nearest centre within `reach`, or `None`."""
    best: tuple[int, int] | None = None
    for index, centre in enumerate(centres):
        dist = distance(point, centre)
        if dist is not None and dist <= reach and (best is None or dist < best[0]):
            best = (dist, index)
    return best[1] if best else None


def assign_talents(talents: Mapping[int, int], builds: BuildsResult | SpecBuilds, scope: TalentScope) -> Build | None:
    """The Build a player's Talents belong to, by the rules the Builds were stored with."""
    settings = builds.settings

    def project(t: Mapping[int, int]) -> _Point:
        return _project(t, scope, settings.ignore, settings.force_new_build)

    index = _assign(
        project(talents),
        [project(build.talents) for build in builds.builds],
        max(settings.threshold, settings.min_assign),
    )
    return None if index is None else builds.builds[index]


def _defining(mains: Sequence[_Point]) -> list[DefiningTalents]:
    result = []
    for index, main in enumerate(mains):
        others = [m.ranks for i, m in enumerate(mains) if i != index]
        if not others:
            result.append(DefiningTalents())
            continue
        has = {entry: rank for entry, rank in sorted(main.ranks) if not any((entry, rank) in o for o in others)}
        lacks = {
            entry: rank for entry, rank in sorted(frozenset.intersection(*others)) if (entry, rank) not in main.ranks
        }
        result.append(DefiningTalents(has=has, lacks=lacks))
    return result


def find_builds(
    pool: Iterable[Mapping[int, int]],
    scope: TalentScope,
    *,
    ignore: Collection[int] = (),
    force_new_build: Collection[int] = (),
) -> BuildsResult:
    """Group the Talents of a pool of Fights into Builds.

    The threshold starts at `START_THRESHOLD` and rises until the Builds (groups with at least `MIN_SHARE` of the pool,
    at most `MAX_BUILDS`) cover `COVER` of it, or `CAP_THRESHOLD` is reached.
    Talents of different hero trees, or differing in a `force_new_build` entry, are never in the same Build.
    """
    ignore, force_new_build = frozenset(ignore), frozenset(force_new_build)
    loadouts = [frozenset((entry, rank) for entry, rank in talents.items() if rank > 0) for talents in pool if talents]
    projected = {loadout: _project(dict(loadout), scope, ignore, force_new_build) for loadout in set(loadouts)}

    total = len(loadouts)
    counts: collections.Counter[_Point] = collections.Counter(projected[loadout] for loadout in loadouts)
    full: dict[_Point, collections.Counter[frozenset[tuple[int, int]]]] = collections.defaultdict(collections.Counter)
    for loadout in loadouts:
        full[projected[loadout]][loadout] += 1

    settings = BuildSettings(
        threshold=START_THRESHOLD,
        ignore=sorted(ignore),
        force_new_build=sorted(force_new_build),
    )
    if not total:
        return BuildsResult(settings=settings)

    threshold = START_THRESHOLD
    while True:
        groups = [g for g in _groups(counts, threshold) if g.count / total >= MIN_SHARE][:MAX_BUILDS]
        if sum(g.count for g in groups) / total >= COVER or threshold >= CAP_THRESHOLD:
            break
        threshold += 1
    settings.threshold = threshold

    centres = [g.centre for g in groups]
    assigned = collections.Counter(
        _assign(point, centres, max(threshold, MIN_ASSIGN)) for point, count in counts.items() for _ in range(count)
    )
    mains = [max(full[c], key=lambda loadout: full[c][loadout]) for c in centres]
    defining = _defining(centres)

    builds = []
    for index, group in enumerate(groups):
        builds.append(
            Build(
                letter=_letter(index),
                fights=assigned[index],
                hero_tree=min(group.centre.group[0], default=None),
                talents=dict(sorted(mains[index])),
                defining=defining[index],
            ),
        )
    return BuildsResult(fights=total, other=assigned[None], settings=settings, builds=builds)


class SpecBuilds(S3Model):
    """The Builds of one spec in the current season of a Game Version."""

    game_version: str
    spec_slug: str
    updated: UTCDatetime = UTC_MIN

    fights: int = 0
    other: int = 0
    settings: BuildSettings
    builds: list[Build] = []

    key: typing.ClassVar[str] = "{game_version}/{table_name}/{season}/{spec_slug}"

    @classmethod
    def get_key(cls, **kwargs: typing.Any) -> str:
        """The current season of the Game Version, unless a season is passed in."""
        if "game_version" in kwargs:
            kwargs["season"] = get_game_version(kwargs["game_version"]).data.season.slug
        return super().get_key(**kwargs)

    @classmethod
    def from_result(cls, game_version: str, spec_slug: str, result: BuildsResult) -> SpecBuilds:
        return cls(
            game_version=game_version,
            spec_slug=spec_slug,
            updated=datetime.datetime.now(datetime.UTC),
            **result.model_dump(),
        )
