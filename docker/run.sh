#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)

if [ -z $CONTEST ]; then
    echo "Please set \$CONTEST to continue. For example, run with \"CONTEST=example_contests/example docker-compose up\""
    exit 0
fi

trap 'kill -TERM $PID' TERM INT

OPTS=${OPTS:-""}
DEBUG=${DEBUG:-false}
if $DEBUG; then
    OPTS+=" -d"
fi

epsilon $OPTS &
PID=$!
wait $PID
trap - TERM INT
wait $PID
EXIT_STATUS=$?

