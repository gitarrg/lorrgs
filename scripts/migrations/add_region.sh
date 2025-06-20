

cd ~/wow/lorrgs

source venv/bin/activate
export PYTHONPATH=.

echo -ne "\033]0;$1\007"

python scripts/migrations/add_region.py $1


# ~/wow/lorrgs/scripts/migrations/add_region.sh Druid
# ~/wow/lorrgs/scripts/migrations/add_region.sh Evoker
# ~/wow/lorrgs/scripts/migrations/add_region.sh Hunter
# ~/wow/lorrgs/scripts/migrations/add_region.sh Mage

# ~/wow/lorrgs/scripts/migrations/add_region.sh Monk
# ~/wow/lorrgs/scripts/migrations/add_region.sh Paladin

# ~/wow/lorrgs/scripts/migrations/add_region.sh Priest
# ~/wow/lorrgs/scripts/migrations/add_region.sh Rogue
# ~/wow/lorrgs/scripts/migrations/add_region.sh Shaman

# ~/wow/lorrgs/scripts/migrations/add_region.sh Warlock
# ~/wow/lorrgs/scripts/migrations/add_region.sh Warrior