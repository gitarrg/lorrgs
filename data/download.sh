#!/usr/bin/env bash


tables=(
    ChrClasses
    ChrSpecialization
    ManifestInterfaceData
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

for table in "${tables[@]}"; do
    wget -O $table.csv "https://wago.tools/db2/$table/csv"
done
