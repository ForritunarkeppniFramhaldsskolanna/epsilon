#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)

AUTOMATIC_JUDGE=${AUTOMATIC_JUDGE:-true}
if $AUTOMATIC_JUDGE; then
    python3 judge/automatic-judge.py $CONTEST/judge.yml 1 &
fi
python3 server/epsilon.py -H 0.0.0.0 $CONTEST
