#!/bin/bash
# -*- Mode: sh; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

LANG=C
PATH=$(pwd)/bin:$PATH

if [ ! -e $(pwd)/bin ]; then
    echo "You must run this script from the top level of the quickly source"
    exit 1
fi

exit_status() {
    if [ $1 -eq 0 ]; then
        echo -e '\e[32mPASSED\e[0m'
    else
        echo -e '\e[31mFAILED\e[0m'
    fi
    exit $1
}

ORIGINAL_DIR=$(pwd)

SCRIPT=$1
TEMPLATE_NAME=$(echo "$SCRIPT" | cut -d/ -f3)
SCRIPT_NAME=$(basename "$SCRIPT")
LOGFILE="$ORIGINAL_DIR/results.log"

rm -f "$LOGFILE"

if [ -d "$SCRIPT" ]; then
    echo -n "Running $TEMPLATE_NAME $SCRIPT_NAME.sh... "
    SCRIPT="$SCRIPT/$SCRIPT_NAME.sh"
elif echo "$SCRIPT_NAME" | grep "\.py$" > /dev/null; then
    # this is actually a python unit test
    echo -n "Running $TEMPLATE_NAME $SCRIPT_NAME... "
    python "$SCRIPT" > "$LOGFILE" 2>&1
    rv=$?
    if [ $rv -ne 0 ]; then
        echo
        cat "$LOGFILE"
    fi
    rm -f "$LOGFILE"
    exit_status $rv
else
    echo -n "Running $TEMPLATE_NAME $SCRIPT_NAME... "
fi

TEMP_SCRIPT_DIR=$(dirname "$SCRIPT")
SCRIPT_DIR=$(cd "$TEMP_SCRIPT_DIR"; pwd)
CMD="$ORIGINAL_DIR/next-cmd.sh"
CMD_OUTPUT="$ORIGINAL_DIR/output.log"
DISPLAY="" # to avoid popup projects when creating them

head -n1 "$SCRIPT" >> "$LOGFILE"
egrep -v '(^#|^\s*$)' "$SCRIPT" | while read line; do
    echo >> "$LOGFILE"
    echo $line >> "$LOGFILE";
    echo "#!/bin/sh" > $CMD;
    echo "export TEST_SCRIPT_DIR=$SCRIPT_DIR" >> $CMD;
    # Piping this line will cause a separate subprocess to execute
    echo "$line &> \"$CMD_OUTPUT\"" >> $CMD;
    source $CMD
    cat "$CMD_OUTPUT" | awk '{print "# " $0}' >> "$LOGFILE";
done

cd "$ORIGINAL_DIR"
rm -f "$CMD"
rm -f "$CMD_OUTPUT"
if [[ -n $(diff -q "$SCRIPT" "$LOGFILE") ]]; then
    echo # The "Running BLAH BLAH... " didn't have a trailing newline
    echo "********************************"
    diff -Nu "$SCRIPT" "$LOGFILE"
    echo "********************************"
    exit_status 1
else
    rm -f "$LOGFILE"
    exit_status 0
fi
