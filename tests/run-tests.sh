#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)


JAIL=${EPSILON_JAIL:-$EPSILON_PREFIX/judge/jail}
SUBS=$EPSILON_PREFIX/judge/submissions
SUB="$SUBS/epsilon-1_1337"

function run_test {
    echo "5" > $SUB/in
    echo "-3" >> $SUB/in
    # user_no normal_user sub_no cpu_seconds mem_kbytes nproc cmd
    sudo -E $EPSILON_PREFIX/judge/execute-submission.sh 1 $(whoami) 1337 3 8000000 30 "$1"
    exit_code=$?
    diff $SUB/out <(echo "2")
    [ $exit_code ] || (echo "error" && exit 1)
    diff <(head -n 1 $SUB/usage) <(echo "OK")
    rm -rf $SUB
}

echo "Python 2"
mkdir $SUB
cp $BASE_DIR/add/sol.py2 $SUB/sol.py
run_test "/usr/bin/python2 sol.py"

echo "Python 3"
mkdir $SUB
cp $BASE_DIR/add/sol.py3 $SUB/sol.py
run_test "/usr/bin/python3 sol.py"

echo "Perl"
mkdir $SUB
cp $BASE_DIR/add/sol.pl $SUB
run_test "/usr/bin/perl sol.pl"

echo "C++"
mkdir $SUB
cd $BASE_DIR/add
g++ -Wall sol.cpp -o a.out
cd ..
mv $BASE_DIR/add/a.out $SUB
run_test "./a.out"

echo "C"
mkdir $SUB
cd $BASE_DIR/add
gcc -Wall sol.c -o a.out
cd ..
mv $BASE_DIR/add/a.out $SUB
run_test "./a.out"

echo "Ruby"
mkdir $SUB
cp $BASE_DIR/add/sol.rb $SUB
run_test "/usr/bin/ruby sol.rb"

echo "Java"
mkdir $SUB
cd $BASE_DIR/add
javac Main.java
cd ..
mv $BASE_DIR/add/Main.class $SUB
run_test "/usr/bin/java Main"

echo "C#"
mkdir $SUB
cd $BASE_DIR/add
dmcs -r:System.Numerics.dll Main.cs
cd ..
mv $BASE_DIR/add/Main.exe $SUB
run_test "/usr/bin/mono Main.exe"

echo "Pascal"
mkdir $SUB
cd $BASE_DIR/add
fpc -osol sol.pas 2>&1 >/dev/null
rm -f sol.o
cd ..
mv $BASE_DIR/add/sol $SUB
run_test "./sol"

echo "JavaScript"
mkdir $SUB
cp $BASE_DIR/add/sol.js $SUB
run_test "/usr/bin/js -f sol.js"

echo "Octave"
mkdir $SUB
cp $BASE_DIR/add/sol.m $SUB
run_test "/usr/bin/octave --silent --no-window-system --no-history --no-init-file --no-line-editing --no-site-file --norc sol.m"

