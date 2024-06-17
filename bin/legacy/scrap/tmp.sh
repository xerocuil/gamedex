#!/usr/bin/env bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SLUG="$1"

cd $SLUG
xmllint --format -o icon-edit.svg -pretty 1 icon.svg
xmllint --format -o logo-edit.svg -pretty 1 logo.svg
mv icon-edit.svg icon.svg
mv logo-edit.svg logo.svg
cd $SCRIPT_DIR