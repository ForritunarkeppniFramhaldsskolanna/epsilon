#!/bin/bash
set -e


BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
EPSILON_DIR=${EPSILON_DIR:-"$BASE_DIR/.."}
eval $(python3 $EPSILON_DIR/config/config.py export)

# If we are supposed to load a contest, setup the aliases
if ! [ -z $CONTEST ]; then
    export CONTEST_PATH=$(cd $CONTEST && pwd)
    echo -e "#!/bin/bash \npython3 $EPSILON_PREFIX/manual_judge/judge.py -c \"$CONTEST_PATH\" \$@" > /usr/local/bin/judge
    echo -e "#!/bin/bash \npython3 $EPSILON_PREFIX/manual_judge/sh.py \"$CONTEST_PATH\" \$@" > /usr/local/bin/judgesh
    echo -e "#!/bin/bash \npython3 $EPSILON_PREFIX/judge/automatic-judge.py \"$CONTEST_PATH\" \$@" > /usr/local/bin/autojudge
    echo -e "#!/bin/bash \npython3 $EPSILON_PREFIX/server/epsilon.py -H 0.0.0.0 \"$CONTEST_PATH\" \$@" > /usr/local/bin/epsilon
else
    echo -e "#!/bin/bash \necho \"You need to set \\\$CONTEST to use this function\"" > /usr/local/bin/judge
    echo -e "#!/bin/bash \necho \"You need to set \\\$CONTEST to use this function\"" > /usr/local/bin/judgesh
    echo -e "#!/bin/bash \necho \"You need to set \\\$CONTEST to use this function\"" > /usr/local/bin/autojudge
    echo -e "#!/bin/bash \necho \"You need to set \\\$CONTEST to use this function\"" > /usr/local/bin/epsilon
fi

chmod +x /usr/local/bin/judge
chmod +x /usr/local/bin/judgesh
chmod +x /usr/local/bin/autojudge
chmod +x /usr/local/bin/epsilon

exec "$@"
