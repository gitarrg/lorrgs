#!/usr/bin/env bash


tables=(
    ChrClasses
    ChrSpecialization
    SpecializationSpells
    SpellName
    SpellCooldowns
)

for table in ${tables[@]}; do
    wget -O $table.csv "https://wago.tools/db2/$table/csv"
done
