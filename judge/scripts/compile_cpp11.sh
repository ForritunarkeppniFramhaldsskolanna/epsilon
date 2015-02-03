#!/bin/sh

FILE="sol.cpp"
DEST="a.out"

# -Wall:	Report all warnings
# -O2:		Level 2 optimizations (default for speed)
# -static:	Static link with all libraries
# -pipe:	Use pipes for communication between stages of compilation
g++ -std=c++11 -Wall -O2 -static -pipe -DONLINE_JUDGE -o "$DEST" "$FILE"
exit $?
