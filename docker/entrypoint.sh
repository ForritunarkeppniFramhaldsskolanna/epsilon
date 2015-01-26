#!/bin/bash

set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)

echo "Mounting directories for jail...."
export JAIL=${EPSILON_JAIL:-$EPSILON_PREFIX/judge/jail}
mkdir -p $JAIL/run
sudo mount -o bind /run $JAIL/run

mkdir -p $JAIL/proc
sudo mount -o bind /proc $JAIL/proc

mkdir -p $JAIL/dev/shm
sudo mount -o bind /dev/shm $JAIL/dev/shm

echo "done"

exec "$@"