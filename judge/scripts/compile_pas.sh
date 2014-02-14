#!/bin/sh

FILE="sol.pas"
DEST="prog"

# -viwn:    Verbose warnings, notes and informational messages
# -02:      Level 2 optimizations (default for speed)
# -Sg:      Support label and goto commands (for those who need it ;-)
# -XS:      Static link with all libraries
fpc -viwn -O2 -Sg -XS -dONLINE_JUDGE -o$DEST "$FILE"
exitcode=$?

# clean created object files:
rm -f $DEST.o

exit $exitcode
