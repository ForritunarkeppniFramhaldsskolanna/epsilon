#!/bin/sh

# ADA compile wrapper-script for 'compile.sh'.
# See that script for syntax and more info.

DEST="$1" ; shift
MEMLIMIT="$1" ; shift
MAINSOURCE="$1"

# -static:         Static link with all libraries
# -bargs -static:  Static link with all libraries
gnatmake -static -o $DEST "$@" -bargs -static
exitcode=$?

# clean created files:
rm -f $DEST.o $DEST.ali

exit $exitcode
