#!/bin/bash

JAIL=__EPSILON_PREFIX__/judge/jail

for ((i=1; i<=__EPSILON_JUDGE_USERS__; i++))
do
    USER=__EPSILON_JUDGE_USER_PREFIX__-$i
    userdel -f $USER
    rm -rf /home/$USER
done

umount -f $JAIL/proc
umount -f $JAIL/run
rm -rf $JAIL

