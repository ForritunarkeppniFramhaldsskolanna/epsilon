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

# If we are supposed to load a contest, setup the aliases
if ! [ -z $CONTEST ]; then
    export CONTEST_PATH=$(cd $CONTEST && pwd)
    echo -e "#!/bin/bash \npython3 $EPSILON_PREFIX/manual_judge/judge.py -c $CONTEST_PATH/judge.yml \$@" > /usr/local/bin/judge
    echo -e "#!/bin/bash \npython3 $EPSILON_PREFIX/judge/automatic-judge.py $CONTEST_PATH/judge.yml \$@" > /usr/local/bin/autojudge
    chmod +x /usr/local/bin/judge
    chmod +x /usr/local/bin/autojudge
else
    echo -e "#!/bin/bash \necho \"You need to set \\\$CONTEST to use this function\"" > /usr/local/bin/judge
    echo -e "#!/bin/bash \necho \"You need to set \\\$CONTEST to use this function\"" > /usr/local/bin/autojudge
    chmod +x /usr/local/bin/judge
    chmod +x /usr/local/bin/autojudge
fi

exec "$@"