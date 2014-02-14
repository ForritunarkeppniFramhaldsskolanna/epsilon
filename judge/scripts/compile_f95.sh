#!/bin/sh

# Fortran compile wrapper-script for 'compile.sh'.
# See that script for syntax and more info.

DEST="$1" ; shift
MEMLIMIT="$1" ; shift
MAINSOURCE="$1"

# -Wall:        Report all warnings
# -02:          Level 2 optimizations (default for speed)
# -static:      Static link with all libraries
# -cpp:         Run C preprocessor
gfortran -static -Wall -O2 -cpp -DONLINE_JUDGE -DDOMJUDGE -o $DEST "$@"
exitcode=$?

# clean created files:
rm -f $DEST.o

exit $exitcode
