#!/bin/sh

FILE="Main.java"
MAINCLASS=""

CMP="compilation"

javac -d . "$FILE" 2> "$CMP"
EXITCODE=$?
if [ "$EXITCODE" -ne 0 ]; then
    # Let's see if should have named the .java differently
    PUBLICCLASS=$(sed -n -e '/class .* is public, should be declared in a file named /{s/.*file named //;s/\.java.*//;p;q}' "$CMP")
    if [ -z "$PUBLICCLASS" ]; then
        cat $CMP
        rm -f $CMP
        exit $EXITCODE
    fi
    rm -f $CMP
    mv "$FILE" "$PUBLICCLASS.java"
    javac -d . "$PUBLICCLASS.java"
    EXITCODE=$?
    [ "$EXITCODE" -ne 0 ] && exit $EXITCODE
fi

rm -f $CMP

# Look for class that has the 'main' function:
for cn in $(find * -type f -regex '^.*\.class$' \
        | sed -e 's/\.class$//' -e 's/\//./'); do
    javap -public "$cn" \
    | egrep -q 'public static (|final )void main\(java.lang.String(\[\]|\.\.\.)\)' \
    && {
        if [ -z "$MAINCLASS" ]; then
            MAINCLASS=$cn
        fi
    }
done
if [ -z "$MAINCLASS" ]; then
    echo "Error: no 'main' found in any class file."
    exit 1
fi

# Write executing script:
# Executes java byte-code interpreter with following options
# -Xmx: maximum size of memory allocation pool
# -Xrs: reduces usage signals by java, because that generates debug
#       output when program is terminated on timelimit exceeded.
cat > "execute.sh" <<EOF
#!/bin/sh
exec /usr/bin/java -Xrs -Xss8m -DONLINE_JUDGE=1 -Xmx1280M -Xms128M $MAINCLASS
EOF

chmod a+x execute.sh

exit 0
