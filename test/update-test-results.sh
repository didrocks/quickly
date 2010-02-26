#!/bin/bash

ORIGINAL_DIR=$(pwd)

SCRIPT=$1
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
    # Piping this line will cause a separate subprocess to execute
    echo "$line &> \"$CMD_OUTPUT\"" >> $CMD;
    source $CMD
    cat "$CMD_OUTPUT" | tee | awk '{print "# " $0}' >> "$LOGFILE";
done

rm -f "$CMD"
rm -f "$CMD_OUTPUT"
mv -f "$LOGFILE" "$SCRIPT"
