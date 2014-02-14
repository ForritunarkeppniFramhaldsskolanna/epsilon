#!/bin/sh

FILE="sol.py"

# Check for '#!' interpreter line: don't allow it to prevent teams
# from passing options to the interpreter.
if grep '^#!' "$FILE" >/dev/null 2>&1 ; then
    echo "Error: interpreter statement(s) found:"
    grep -n '^#!' "$FILE"
    exit 1
fi

python3 -c "compile(open('sol.py').read(), 'sol.py', 'exec')"
exit $?
