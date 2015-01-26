#!/bin/bash
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
eval $(python3 $BASE_DIR/../config/config.py export)

python3 judge/automatic-judge.py test_contests/fk_2014_beta/judge.yml 1 &
python3 server/epsilon.py -H 0.0.0.0 test_contests/fk_2014_beta
