"""Endpoints for the Talent trees of the specs."""

from __future__ import annotations

# IMPORT THIRD PARTY LIBRARIES
import fastapi

# IMPORT LOCAL LIBRARIES
from lorgs.data import talent_trees
from lorrgs_api.dependencies import GameVersionDep


router = fastapi.APIRouter(tags=["talents"], prefix="/talent_trees")


@router.get("/{spec_slug}")
async def get_talent_tree(game_version: GameVersionDep, spec_slug: str) -> dict:
    """The talent tree of one spec: nodes, entries, edges and the node order of the import string.

    Entries are talent node entry ids, as stored in the Talents of a Spec Ranking player.
    Talents of older patches can hold entries missing here.
    """
    spec = game_version.data.get_spec(spec_slug) if game_version.has_talents else None
    tree = talent_trees.get_spec_tree(spec.id) if spec else None
    if tree is None:
        raise fastapi.HTTPException(status_code=404, detail="Not found.")
    return tree
