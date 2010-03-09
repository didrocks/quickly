#!/bin/bash

LANG=C
PATH=$(pwd)/bin:$PATH

ORIGINAL_DIR=$(pwd)

SCRIPT=$1
TEMP_SCRIPT_DIR=$(dirname "$SCRIPT")
SCRIPT_DIR=$(cd "$TEMP_SCRIPT_DIR"; pwd)
LOGFILE="$ORIGINAL_DIR/results.log"
CMD="$ORIGINAL_DIR/next-cmd.sh"
CMD_OUTPUT="$ORIGINAL_DIR/output.log"

rm -f "$LOGFILE"
head -n1 "$SCRIPT" >> "$LOGFILE"
egrep -v '(^#|^\s*$)' "$SCRIPT" | while read line; do
    echo $line
    echo >> "$LOGFILE"
    echo $line >> "$LOGFILE";
    echo "#!/bin/bash" > $CMD;
    echo "export TEST_SCRIPT_DIR=$SCRIPT_DIR" >> $CMD;
    # Piping this line will cause a separate subprocess to execute
    echo "$line &> \"$CMD_OUTPUT\"" >> $CMD;
    source $CMD
    cat "$CMD_OUTPUT" | tee | awk '{print "# " $0}' >> "$LOGFILE";
done

cd "$ORIGINAL_DIR"
rm -f "$CMD"
rm -f "$CMD_OUTPUT"
if [[ -n $(diff -q "$LOGFILE" "$SCRIPT") ]]; then
    echo "********************************"
    echo "FILES DIFFERED"
    diff -Nup "$LOGFILE" "$SCRIPT"
    echo -n "Would you like to accept the new results (y/n)? [y] "
    read -n1 RESULT
    echo
    if [[ "$RESULT" = "y" || "$RESULT" = "" ]]; then
        mv -f "$LOGFILE" "$SCRIPT"
    fi
else
    rm -f "$LOGFILE"
fi
