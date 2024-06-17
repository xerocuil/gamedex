#!/usr/bin/env bash

APPDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DEVICE_DIR="/run/media/$USER/ROMS"
LOCAL_CFW=$(dirname "$APPDIR/CFW")
DEVICE_CFW="$DEVICE_DIR/CFW"

CMD="$1"

clean(){
    echo "Checking directories..."
    # Clean directories
    find "$LOCAL_CFW" "$DEVICE_DIR"\
     -depth\
     -type d \( \
     -name .dtrash \
     -o -name .Trash-1000 \
     -o -name __pycache__ \
     \)\
     -exec rm -rf "{}" \;

    # Clean files
    find "$LOCAL_CFW"\
     -depth\
     -type f\
     -name "*.bak"\
     -name "*.tmp"\
     -exec rm -rf "{}" \;
    echo "Done."
}

help(){
    printf "
## Usage: start.sh [COMMAND]

If no command is given, the script will run application.

## COMMANDS

Command     | Description
:------     | :----------
clean       | Clean directories application.


"
}

if [[ -z $CMD ]]; then
    help
else
    if ! $CMD; then
        help
    fi
fi
