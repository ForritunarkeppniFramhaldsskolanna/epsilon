#!/bin/sh

FILE="Main.cs"
DEST="Main.exe"

dmcs -o+ -d:ONLINE_JUDGE -r:System.Numerics.dll -out:"$DEST" "$FILE"
exit $?
