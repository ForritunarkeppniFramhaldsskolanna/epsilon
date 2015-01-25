#!/bin/bash
eval $(python3 ../config/config.py export)
JAIL=$EPSILON_PREFIX/judge/jail
DIR=$PSILON_PREFIX/judge

# TODO: this isn't very neat, maybe copy safeexec manually into the jail?
#cp $DIR/SafeExec/safeexec /usr/bin/safeexec

#ln -s /bin/sh /usr/bin/sh
#ln -s /bin/bash /usr/bin/bash
#ln -s /usr/sbin/locale-gen /usr/bin/locale-gen

jk_init -v -c $EPSILON_PREFIX/config/config.ini -j $JAIL basicshell locale ldconfig safeexec python2 python3 java mono perl ruby fpc js octave

chmod g-w $JAIL/etc

# TODO: can I remove this?
chmod +s $JAIL/usr/bin/safeexec
#rm -f /usr/bin/safeexec # TODO: same as above.

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
cp $JAIL/usr/lib/jvm/java-7-openjdk/jre/lib/amd64/jli/libjli.so $JAIL/lib/
cp $JAIL/usr/lib/jvm/java-7-openjdk-i386/jre/lib/i386/jli/libjli.so $JAIL/lib/
cp $JAIL/usr/lib/jvm/java-7-openjdk/jre/lib/amd64/libjava.so $JAIL/lib/
cp $JAIL/usr/lib/jvm/java-7-openjdk-i386/jre/lib/i386/libjava.so $JAIL/lib/

# For Octave
#cp $JAIL/usr/lib/openmpi/* $JAIL/usr/lib
cp $JAIL/usr/lib/libblas.so.3 $JAIL/usr/lib/libblas.so.3gf
cp $JAIL/usr/lib/liblapack.so.3 $JAIL/usr/lib/liblapack.so.3gf

for ((i=1; i<=$EPSILON_JUDGE_USERS; i++))
do
    USER=$EPSILON_JUDGE_USER_PREFIX-$i
    useradd -d /home/$USER -m -U -s $EPSILON_EXE_BASH $USER
    jk_jailuser -m -j $JAIL -s $EPSILON_EXE_BASH $USER
    chmod 755 $JAIL/home/$USER
done

jk_chrootlaunch -j $JAIL -u root -x $EPSILON_EXE_LOCALE_GEN
jk_chrootlaunch -j $JAIL -u root -x $EPSILON_EXE_LDCONFIG

