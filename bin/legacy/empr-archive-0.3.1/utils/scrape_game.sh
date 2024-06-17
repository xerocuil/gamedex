#! /bin/bash

UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $UTILS/utils.sh

SCRAPERDIR=$UTILS/scrapers
BACKUPDIR=/opt/empr/docs/backup
GBSCRAPER=$SCRAPERDIR/gb/gb_scraper.sh
SKYSCRAPER=$SCRAPERDIR/ss/skyscraper.sh
TGDBSCRAPER=$SCRAPERDIR/tgdb/tgdb_scraper.sh

FILE="$1"
FILEPATH=$(readlink -f "$FILE")
FILENAME=$(basename $FILEPATH)
SLUG=${FILENAME%.*}
PLATFORMDIR="$(dirname $FILE)"
PLATFORM_SLUG=$(basename $PLATFORMDIR)
ASSETDIR="$CACHEDIR/assets/$SLUG"

echo -e "\nClearing cache...\n"
if [[ -d  $CACHEDIR/assets ]]; then
	echo "Clearing cache directory..."
	rm -rf $CACHEDIR/*
fi

mkdir -p $ASSETDIR

echo "
Scraping $FILENAME ..."

$TGDBSCRAPER "$FILE"
$GBSCRAPER "$FILE"

if [[ $PLATFORM_SLUG = "32x" ]]; then
	SS_SLUG="sega32x"
elif [[ $PLATFORM_SLUG = "3d0" ]]; then
	SS_SLUG="3do"
elif [[ $PLATFORM_SLUG = "atari-2600" ]]; then
	SS_SLUG="atari2600"
elif [[ $PLATFORM_SLUG = "jaguar" ]]; then
	SS_SLUG="atarijaguar"
elif [[ $PLATFORM_SLUG = "gg" ]]; then
	SS_SLUG="gamegear"
elif [[ $PLATFORM_SLUG = "gamecube" ]]; then
	SS_SLUG="gc"
elif [[ $PLATFORM_SLUG = "ps1" ]]; then
	SS_SLUG="psx"
elif [[ $PLATFORM_SLUG = "sms" ]]; then
	SS_SLUG="mastersystem"
elif [[ $PLATFORM_SLUG = "neo-geo" ]]; then
	SS_SLUG="neogeo"
elif [[ $PLATFORM_SLUG = "turboduo" ]]; then
	SS_SLUG="pcengine"
elif [[ $PLATFORM_SLUG = "sega-cd" ]]; then
	SS_SLUG="segacd"
elif [[ $PLATFORM_SLUG = "vb" ]]; then
	SS_SLUG="virtualboy"
elif [[ $PLATFORM_SLUG = "wii-u" ]]; then
	SS_SLUG="wiiu"
else
	SS_SLUG="$PLATFORM_SLUG"
fi

skyscraper -p $SS_SLUG -s screenscraper $FILEPATH
skyscraper -p $SS_SLUG $FILEPATH
$SKYSCRAPER "$FILE"

gb_description=$ASSETDIR/gb-$SLUG-description.txt
ss_description=$ASSETDIR/ss-$SLUG-description.txt
tgdb_description=$ASSETDIR/tgdb-$SLUG-description.txt

gb_details=$ASSETDIR/gb-$SLUG-details.txt
ss_details=$ASSETDIR/ss-$SLUG-details.txt
tgdb_details=$ASSETDIR/tgdb-$SLUG-details.txt

echo "
DESCRIPTIONS:

[GB]
$(cat $gb_description)
---

[SS]
$(cat $ss_description)
---

[TGDB]
$(cat $tgdb_description)
---
"

title=$(cat $tgdb_details | grep -m 1 "title:" | cut -d ":" -f 2 | xargs)
sort_title=$(cat $tgdb_details | grep "sort_title:" | cut -d ":" -f 2 | xargs)
path=$FILENAME
platform=$(cat $ss_details | grep "platform:" | cut -d ":" -f 2 | xargs)
platform_slug=$(cat $ss_details | grep "platform_slug:" | cut -d ":" -f 2 | xargs)
genre=$(cat $tgdb_details | grep "genre:" | cut -d ":" -f 2 | xargs)
developer=$(cat $tgdb_details | grep "developer:" | cut -d ":" -f 2 | xargs)
publisher=$(cat $tgdb_details | grep "publisher:" | cut -d ":" -f 2 | xargs)
release_date=$(cat $tgdb_details | grep "release_date:" | cut -d ":" -f 2 | xargs)
release_year=${release_date:0:4}
players=$(cat $ss_details | grep "players:" | cut -d ":" -f 2 | xargs)
description="$(cat $gb_description)"

echo "
title: $title
sort_title: $sort_title
path: $FILENAME

platform: $platform
platform_slug: $platform_slug

genre: $genre

developer: $developer
publisher: $publisher

release_date: $release_year
players: $players
"

rm $ASSETDIR/*.txt

firefox "$LOCALURL/game/scrape/?path=$path&title=$title&sort_title=$sort_title&developer=$developer&publisher=$publisher&release_date=$release_year&path=$path&description=$description" &
