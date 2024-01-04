#!/bin/sh

PATH_TO_JC="$SNAP/bin/jc"

# Don't work. I don't know why.
# if [ -w "$SNAP_REAL_HOME/.local/share/jc" ] ; then

if ls "$SNAP_REAL_HOME/.local/share/jc" 1>/dev/null 2>/dev/null
then
    HOME="$SNAP_REAL_HOME" "$PATH_TO_JC" "$@";
else
    "$PATH_TO_JC" "$@";
fi
