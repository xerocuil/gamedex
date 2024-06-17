#! /bin/bash

source /opt/empr/utils/utils.sh
FILENAME=$1
SLUG="${FILENAME%.*}"
MEDIADIR=$HOME/.empr/media
STEAMASSETS=$MEDIADIR/steam
HEADER_TEMPLATE=$CMS/static/imgs/header.png

id_query(){
  $SQLITE $APPDB "select id from games_game where path = '$FILENAME';"
}

ID=$(id_query)

if [[ -z $ID ]];then
  echo "$FILENAME not found in database."
  exit
fi

platform_id=$(sqlite3 $APPDB "select platform_id from games_game where id = '$ID';")
platform_icon=$(sqlite3 $APPDB "select icon from games_platform where id = '$platform_id';")
platform_name=$(sqlite3 $APPDB "select name from games_platform where id = '$platform_id';")
platform_slug=$(sqlite3 $APPDB "select slug from games_platform where id = '$platform_id';")
title=$(sqlite3 $APPDB  "select title from games_game where id = '$ID'")
boxart=$(sqlite3 $APPDB  "select boxart from games_game where id = '$ID'")
wallpaper=$(sqlite3 $APPDB  "select wallpaper from games_game where id = '$ID'")
title_image=$(sqlite3 $APPDB "select title_image from games_game where id = '$ID'")

STASSETDIR=$STEAMASSETS/$SLUG
mkdir -p $STASSETDIR

if [[ ! -f ~/.icons/$platform_slug.png ]]; then
  printf "No platform icon.\n"
  cp -v $MEDIADIR/$platform_icon ~/.icons/$platform_slug.png
fi

printf "Checking for background image..."
if [[ -z $wallpaper ]]; then
  printf " none found.\n"
else
  printf " found.\n"
  cp -v "$MEDIADIR/$wallpaper" "$STASSETDIR/background.png"
fi

printf "Checking for boxart..."
if [[ -z $boxart ]]; then
  printf " none found.\n"
else
  printf " found.\n"
  convert "$MEDIADIR/$boxart" "$STASSETDIR/boxart.png"
fi

printf "Checking for logo..."
if [[ -z $title_image ]]; then
  printf " none found.\n"
  exit
else
  printf " found. Creating header.\n"
  convert "$MEDIADIR/$title_image" -resize 415x194\> "$CACHEDIR/$SLUG-title.png"
  composite -gravity center "$CACHEDIR/$SLUG-title.png" "$HEADER_TEMPLATE" "$STASSETDIR/grid.png"
  rm "$CACHEDIR/$SLUG-title.png"
fi

printf "Creating DCF.\n"
DCFILE="$STASSETDIR/$SLUG.desktop"

printf "[Desktop Entry]
Encoding=UTF-8
Name=$title
Comment=$platform_name game
Type=Application
Exec=rom-launcher.sh $platform_slug /home/player1/Games/roms/$platform_slug/$FILENAME
Icon=$platform_slug
Categories=Game;"  >$DCFILE
chmod +x $DCFILE

# cp -v $DCFILE $HOME/.local/share/applications/

printf "
ID: $ID
title: $title
platform_id: $platform_id
platform_icon: $platform_icon
platform_name: $platform_name
platform_slug: $platform_slug
"