#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)

JAIL=${EPSILON_JAIL:-$EPSILON_PREFIX/judge/jail}

for ((i=1; i<=$EPSILON_JUDGE_USERS; i++))
do
    USER=$EPSILON_JUDGE_USER_PREFIX-$i
    userdel -f $USER
    rm -rf /home/$USER
done

umount -f $JAIL/proc
umount -f $JAIL/run
rm -rf $JAIL

