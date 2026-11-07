#!/usr/bin/env bash
# Download the DB2 tables we read from wago.tools.
#
#   data/download.sh        Retail (current build) into data/
#   data/download.sh wowf   WoW Forever (its newest build) into data/wowf/

set -euo pipefail
cd "$(dirname "$0")"

product="${1:-}"

if [ -z "$product" ]; then
    query=""
    tables=(
        ChrClasses
        ChrSpecialization
        ManifestInterfaceData
        MapChallengeMode
        SpecializationSpells
        SpellMisc
        SpellName
        SpellCooldowns
        SpecSetMember
        TraitCond
        TraitDefinition
        TraitEdge
        TraitNode
        TraitNodeEntry
        TraitNodeGroupXTraitCond
        TraitNodeGroupXTraitNode
        TraitNodeXTraitCond
        TraitNodeXTraitNodeEntry
        TraitSubTree
        TraitTree
        TraitTreeLoadout
    )
else
    build=$(curl -sf https://wago.tools/api/builds | jq -r --arg p "$product" '.[$p][0].version')
    echo "$product build $build"
    query="?build=$build"
    mkdir -p "$product"
    cd "$product"
    # see `lorgs/data/tab_talent_trees.py`
    tables=(
        ManifestInterfaceData
        SpellMisc
        SpellName
        TraitCond
        TraitCurrency
        TraitDefinition
        TraitEdge
        TraitNode
        TraitNodeEntry
        TraitNodeGroupXTraitCond
        TraitNodeGroupXTraitNode
        TraitNodeXTraitNodeEntry
        TraitTreeXTraitCurrency
    )
fi

for table in "${tables[@]}"; do
    wget -O "$table.csv" "https://wago.tools/db2/$table/csv$query"
done
