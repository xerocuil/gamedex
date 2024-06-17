#!/bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRAPERS="$(dirname $DIR)"
UTILS="$(dirname $SCRAPERS)"
source $UTILS/utils.sh

MEDIADIR=$CMSDIR/media
SCRAPERDIR=$UTILSDIR/scrapers
SKYSCRAPERDIR=$HOME/.empr/screenscraper/import
PATH="$1"
FILENAME=${PATH##*/}
SLUG=${FILENAME%.*}


id_query(){
	$SQLITE "$APPDB" "select id from games_game where path = '$FILENAME'"
}

ID=$(id_query)

echo "
PATH: $PATH"

if [[ -z $ID ]];then
  echo "$FILENAME not found in database."
  exit
fi

title=$($SQLITE "$APPDB" "select title from games_game where id = '$ID'")
sort_title=$($SQLITE "$APPDB" "select sort_title from games_game where id = '$ID'")
platform_id=$($SQLITE "$APPDB" "select platform_id from games_game where id = '$ID'")
platform_name=$($SQLITE "$APPDB" "select name from games_platform where id = '$platform_id'")
platform_slug=$($SQLITE "$APPDB" "select slug from games_platform where id = '$platform_id'")
description=$($SQLITE "$APPDB" "select description from games_game where id = '$ID'")
esrb=$($SQLITE "$APPDB" "select esrb from games_game where id = '$ID'")
developer=$($SQLITE "$APPDB" "select developer from games_game where id = '$ID'")
publisher=$($SQLITE "$APPDB" "select publisher from games_game where id = '$ID'")
genre_id=$($SQLITE "$APPDB" "select genre_id from games_game where id = '$ID'")
genre_name=$($SQLITE "$APPDB" "select name from games_genre where id = '$genre_id'")
player=$($SQLITE "$APPDB" "select player from games_game where id = '$ID'")
release_date=$($SQLITE "$APPDB" "select release_date from games_game where id = '$ID'")

controller_support=$($SQLITE "$APPDB" "select controller_support from games_game where id = '$ID'")

notes=$($SQLITE "$APPDB" "select notes from games_game where id = '$ID'")

boxart=$($SQLITE "$APPDB" "select boxart from games_game where id = '$ID'")
screenshot=$($SQLITE "$APPDB" "select screenshot from games_game where id = '$ID'")
title_image=$($SQLITE "$APPDB" "select title_image from games_game where id = '$ID'")
wallpaper=$($SQLITE "$APPDB" "select wallpaper from games_game where id = '$ID'")


date_added=$($SQLITE "$APPDB" "select date_added from games_game where id = '$ID'")
date_modified=$($SQLITE "$APPDB" "select date_modified from games_game where id = '$ID'")

mkdir -p $SKYSCRAPERDIR/$platform_slug
mkdir -p $SKYSCRAPERDIR/$platform_slug/covers 

echo -e "<game>
  <title>$title</title>
  <description>$description</description>
  <developer>$developer</developer>
  <publisher>$publisher</publisher>
  <players>$player</players>
  <genre>$genre_name</genre>
  <releasedate>$release_date</releasedate>
</game>" >$SKYSCRAPERDIR/$platform_slug/textual/$SLUG.xml

## Get Images

if [[ -f $MEDIADIR/$boxart ]]; then
	/usr/bin/cp -v $MEDIADIR/$boxart $SKYSCRAPERDIR/$platform_slug/covers/$SLUG.jpg
fi

if [[ -f $MEDIADIR/$screenshot ]]; then
	/usr/bin/cp -v $MEDIADIR/$screenshot $SKYSCRAPERDIR/$platform_slug/screenshots/$SLUG.jpg
else
	/usr/bin/cp -v $MEDIADIR/$wallpaper $SKYSCRAPERDIR/$platform_slug/screenshots/$SLUG.jpg
fi

if [[ -f $MEDIADIR/$title_image ]]; then
	/usr/bin/cp -v $MEDIADIR/$title_image $SKYSCRAPERDIR/$platform_slug/wheels/$SLUG.png
fi

echo -e "
## REPORT ##

ID: $ID
FILENAME: $FILENAME
SLUG: $SLUG

title: $title
sort_title: $sort_title

platform_name: $platform_name
platform_slug: $platform_slug

developer: $developer
publisher: $publisher
release_date: $release_date
players: $player
esrb: $esrb
genre_id: $genre_id
genre: $genre_name

description:
$description

notes:
$notes

boxart: $boxart
icon: $icon
wallpaper: $wallpaper

controller_support: $controller_support

date_added: $date_added
date_modified: $date_modified
"