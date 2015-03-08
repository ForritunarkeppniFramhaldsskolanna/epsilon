#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

cd $CONTEST/problems/$1

mkdir -p submissions/accepted submissions/wrong_answer problem_statement input_format_validators data/sample data/secret
mv solution*tle* submissions/wrong_answer
mv solution*wa* submissions/wrong_answer
mv solution* submissions/accepted
cp $BASE_DIR/problem.yaml $CONTEST/problems/$1
mv statement.md problem_statement/problem.en.tex
cp -r assets/* problem_statement
rm -rf assets
python $BASE_DIR/problem.py
rm problem.yml

cp $CONTEST/tests/$1/* data/secret
cd data/secret
for x in *.out; do mv -- "$x" "${x%.out}.ans"; done
cd ../../

echo -e "import sys\nsys.exit(42)" > input_format_validators/validator.py
