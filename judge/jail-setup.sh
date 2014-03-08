#!/bin/bash

JAIL=__EPSILON_PREFIX__/judge/jail
DIR=__EPSILON_PREFIX__/judge

# TODO: this isn't very neat, maybe copy safeexec manually into the jail?
cp $DIR/SafeExec/safeexec /usr/bin/safeexec

#ln -s /bin/sh /usr/bin/sh
#ln -s /bin/bash /usr/bin/bash
#ln -s /usr/sbin/locale-gen /usr/bin/locale-gen

jk_init -v -c $DIR/config.ini -j $JAIL basicshell locale safeexec python2 python3 java mono perl ruby fpc js octave

chmod g-w $JAIL/etc

chmod +s $JAIL/usr/bin/safeexec
rm -f /usr/bin/safeexec # TODO: same as above.

mkdir $JAIL/tmp
chmod a+rwx $JAIL/tmp

# for safeexec semaphore
mkdir -p $JAIL/dev/shm
chmod a+rwx $JAIL/dev/shm

# TODO: mounting run and proc is kind of a security issue...
mkdir -p $JAIL/run
mount -o bind /run $JAIL/run

mkdir $JAIL/proc
mount /proc $JAIL/proc -t proc

# For Java
#cp $JAIL/usr/lib/jvm/java-7-openjdk/jre/lib/amd64/jli/libjli.so $JAIL/lib/

# For Octave
#cp $JAIL/usr/lib/openmpi/* $JAIL/usr/lib

for ((i=1; i<=__EPSILON_JUDGE_USERS__; i++))
do
    USER=__EPSILON_JUDGE_USER_PREFIX__-$i
    useradd -d /home/$USER -m -U -s __EPSILON_EXE_BASH__ $USER
    jk_jailuser -m -j $JAIL -s __EPSILON_EXE_BASH__ $USER
    chmod 755 $JAIL/home/$USER
done

jk_chrootlaunch -j $JAIL -u root -x __EPSILON_EXE_LOCALE_GEN__

