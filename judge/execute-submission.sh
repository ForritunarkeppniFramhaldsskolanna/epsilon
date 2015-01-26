#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)

USER=$1
NORMAL_USER=$2
SUB_ID=$3
CMD=$7

CPU=$4            # seconds
MEM=$5            # kbytes
CORE=0            # kbytes
NPROC=$6          # proccesses
FSIZE=8192        # kbytes
STACK=8192        # kbytes
CLOCK=60          # seconds

# make sure input isn't harmful
! [[ $USER =~ ^[0-9]+$ ]] && exit 1
! [[ $SUB_ID =~ ^[0-9]+$ ]] && exit 1

USER="$EPSILON_JUDGE_USER_PREFIX-$USER"
SUB_ID="${USER}_$SUB_ID"
JAIL=${EPSILON_JAIL:-$EPSILON_PREFIX/judge/jail}
SUBMISSIONS=$EPSILON_PREFIX/judge/submissions

rm -rf "$JAIL/home/$USER/$SUB_ID"
cp -r "$SUBMISSIONS/$SUB_ID" "$JAIL/home/$USER"
chown -R "$USER:$USER" "$JAIL/home/$USER/$SUB_ID"
chmod -R a+r "$JAIL/home/$USER/$SUB_ID"       # TODO: is this really necessary?
chmod -f a+x "$JAIL/home/$USER/$SUB_ID/a.out" # TODO: is this really necessary?
chmod -f a+x "$JAIL/home/$USER/$SUB_ID/Main.exe" # TODO: is this really necessary?
chmod -f a+x "$JAIL/home/$USER/$SUB_ID/execute.sh" # TODO: is this really necessary?
chmod -f a+x "$JAIL/home/$USER/$SUB_ID/prog" # TODO: is this really necessary?

# jk_chrootlaunch -j "$JAIL" -u "$USER" -x /bin/bash -- -c "
#     cd /home/$USER/$SUB_ID
#     /opt/epsilon/judge/bin/SafeExec/safeexec \
#         --usage /tmp/usage-$USER \
#         --cpu $CPU \
#         --mem $MEM \
#         --core $CORE \
#         --nproc $NPROC \
#         --fsize $FSIZE \
#         --stack $STACK \
#         --clock $CLOCK \
#         --exec $CMD <in 1>out 2>err
# "

su "$USER" -c "
    export LANG=\"en_US.UTF-8\"
    cd /home/$USER/$SUB_ID
    $EPSILON_EXE_SAFEEXEC \
        --usage /tmp/usage-$USER \
        --cpu $CPU \
        --mem $MEM \
        --core $CORE \
        --nproc $NPROC \
        --fsize $FSIZE \
        --stack $STACK \
        --clock $CLOCK \
        --exec $CMD <in 1>out 2>err
"

ret=$?

mv $JAIL/home/$USER/$SUB_ID/{out,err} "$SUBMISSIONS/$SUB_ID"
mv "$JAIL/tmp/usage-$USER" "$SUBMISSIONS/$SUB_ID/usage"
chown "$NORMAL_USER" "$SUBMISSIONS/$SUB_ID/out"
chown "$NORMAL_USER" "$SUBMISSIONS/$SUB_ID/err"
chown "$NORMAL_USER" "$SUBMISSIONS/$SUB_ID/usage"
rm -rf "$JAIL/home/$USER/$SUB_ID"

exit $ret

