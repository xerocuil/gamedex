#! /bin/bash

UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APPDIR="$(dirname $UTILS)"
MENUDIR="$HOME/.local/share/applications"
source $UTILS/utils.sh

## PC Games
rm -rf "$ROMSDIR/pc"
mkdir -p "$ROMSDIR/pc"
# cd $PCDIR
for game in $(ls -1 $PCDIR)
do
  if [[ -f "$PCDIR/$game/start.sh" ]]; then
    echo -e "#! /bin/bash\nsh $PCDIR/$game/start.sh" >"$ROMSDIR/pc/$game.sh"
    chmod +x "$ROMSDIR/pc/$game.sh"
  fi
done

## Steam Games
rm -rf "$ROMSDIR/steam"
mkdir -p "$ROMSDIR/steam"
cd $MENUDIR
for file in *
do
  sq=$(cat "$file" | grep "steam://rungameid/")
  if [[ ! -z $sq ]]; then
    steam_id=$(echo "$sq" | cut -f 4 -d "/")
    echo "steam_id: $steam_id"
    path=$(sqlite3 "$APPDB" "select path from games_game where steam_id = '$steam_id'";)
    echo -e "#! /bin/bash\nsteam -silent -applaunch $steam_id" >"$ROMSDIR/steam/$path"
    chmod +x "$ROMSDIR/steam/$path"
  fi
done
