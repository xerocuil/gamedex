#! /bin/bash

UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $UTILS/utils.sh

# PLATFORMS=($(sqlite3 "$APPDB" "select slug from games_platform";))

ARCHIVEROMS="$ARCHIVEDIR/roms"

echo -e "ROMSDIR: $ROMSDIR\nARCHIVEDIR: $ARCHIVEDIR"

for platform in $(ls -1 $ARCHIVEROMS/)
do
  mkdir -p "$ROMSDIR/$platform"
  rsync -hir --ignore-existing --progress "$ARCHIVEROMS/$platform/" "$ROMSDIR/$platform/"
done