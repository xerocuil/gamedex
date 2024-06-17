#!/bin/bash
SRCDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# APPDIR=$(dirname $MAINDIR)
# export WEBKIT_DISABLE_DMABUF_RENDERER=1
cd "$SRCDIR"
pipenv run main
