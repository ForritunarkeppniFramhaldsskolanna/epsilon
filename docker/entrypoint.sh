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
# This is somewhat insecure, but may use less memory
# sudo mount -o bind /dev/shm $JAIL/dev/shm
sudo mount -t tmpfs tmpfs $JAIL/dev/shm

echo "done"

if ! [ -z $CONTEST ]; then
    alias judge="python3 $EPSILON_PREFIX/manual_judge/judge.py -c $(cd $EPSILON_PREFIX/$CONTEST && pwd)/judge.yml"
fi

exec "$@"