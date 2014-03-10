#!/bin/bash

DIR=/opt/epsilon
SUBS=$DIR/judge/submissions
SUB="$SUBS/epsilon-1_1337"

function run_test {
    echo "5" > $SUB/in
    echo "-3" >> $SUB/in
    # user_no normal_user sub_no cpu_seconds mem_kbytes nproc cmd
    sudo $DIR/judge/execute-submission.sh 1 $(whoami) 1337 3 8000000 30 "$1"
    exit_code=$?
    diff $SUB/out <(echo "2")
    [ $exit_code ] || (echo "error" && exit 1)
    diff <(head -n 1 $SUB/usage) <(echo "OK")
    rm -rf $SUB
}

echo "Python 2"
mkdir $SUB
cp add/sol.py2 $SUB/sol.py
run_test "/bin/lang/python2 sol.py"

echo "Python 3"
mkdir $SUB
cp add/sol.py3 $SUB/sol.py
run_test "/bin/lang/python3 sol.py"

echo "Perl"
mkdir $SUB
cp add/sol.pl $SUB
run_test "/bin/lang/perl sol.pl"

echo "C++"
mkdir $SUB
cd add
g++ -Wall sol.cpp -o a.out
cd ..
mv add/a.out $SUB
run_test "./a.out"

echo "C"
mkdir $SUB
cd add
gcc -Wall sol.c -o a.out
cd ..
mv add/a.out $SUB
run_test "./a.out"

echo "Ruby"
mkdir $SUB
cp add/sol.rb $SUB
run_test "/bin/lang/ruby sol.rb"

echo "Java"
mkdir $SUB
cd add
javac Main.java
cd ..
mv add/Main.class $SUB
run_test "/bin/lang/java Main"

echo "C#"
mkdir $SUB
cd add
dmcs -r:System.Numerics.dll Main.cs
cd ..
mv add/Main.exe $SUB
run_test "/bin/lang/mono Main.exe"

echo "Pascal"
mkdir $SUB
cd add
fpc -osol sol.pas 2>&1 >/dev/null
rm -f sol.o
cd ..
mv add/sol $SUB
run_test "./sol"

echo "JavaScript"
mkdir $SUB
cp add/sol.js $SUB
run_test "/bin/lang/js -f sol.js"

echo "Octave"
mkdir $SUB
cp add/sol.m $SUB
run_test "/bin/lang/octave --silent --no-window-system --no-history --no-init-file --no-line-editing --no-site-file --norc sol.m"

