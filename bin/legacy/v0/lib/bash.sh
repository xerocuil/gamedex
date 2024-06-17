#!/usr/bin/env bash

LIB_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
APPDIR=$(dirname "$LIB_DIR")

CMD="$1"

clean(){
    echo "Checking directories..."
    # Clean directories
    find "$APPDIR"\
     -depth\
     -type d \( \
     -name .dtrash \
     -o -name __pycache__ \
     \)\
     -exec rm -rf "{}" \;
}

install_deps(){
    sudo pacman -S python cairo pkgconf gobject-introspection gtk4
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
