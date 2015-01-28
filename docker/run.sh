#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)

if [ -z $CONTEST ]; then
    echo "Please set \$CONTEST to continue. For example, run with \"CONTEST=example_contests/example docker-compose up\""
    exit 0
fi

AUTOMATIC_JUDGE=${AUTOMATIC_JUDGE:-true}
if $AUTOMATIC_JUDGE; then
    autojudge 1 &
fi
python3 server/epsilon.py -H 0.0.0.0 $CONTEST
