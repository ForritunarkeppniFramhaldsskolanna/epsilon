#!/bin/sh

FILE="sol.c"
DEST="a.out"

# -Wall:	Report all warnings
# -O2:		Level 2 optimizations (default for speed)
# -static:	Static link with all libraries
# -pipe:	Use pipes for communication between stages of compilation
# -lm:		Link with math-library (has to be last argument!)
gcc -Wall -O2 -static -pipe -DONLINE_JUDGE -o "$DEST" "$FILE" -lm
exit $?
