#! /bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRAPERS="$(dirname $DIR)"
UTILS="$(dirname $SCRAPERS)"
source $UTILS/utils.sh

FILE=$1
FILEPATH=$(readlink -f "$FILE")
PLATFORMDIR="$(dirname $FILE)"
PLATFORM_SLUG=$(basename $PLATFORMDIR)

QUICKIDXML="$HOME/.empr/skyscraper/cache/$PLATFORM_SLUG/quickid.xml"
DBXML="$HOME/.empr/skyscraper/cache/$PLATFORM_SLUG/db.xml"

echo "
QUICKIDXML: $QUICKIDXML
DBXML: $DBXML
"

XMLPATHQUERY="string(/quickids/quickid[@filepath='$FILEPATH']/@id)"
XMLIDQUERY=$(xmllint --xpath "$XMLPATHQUERY" $QUICKIDXML)

TITLE_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='title']/text()"
PLATFORM_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='platform']/text()"
DEVELOPER_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='developer']/text()"
PUBLISHER_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='publisher']/text()"
PLAYERS_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='players']/text()"
AGES_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='ages']/text()"
TAGS_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='tags']/text()"
RELEASEDATE_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='releasedate']/text()"
COVER_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='cover']/text()"
SCREENSHOT_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='screenshot']/text()"
WHEEL_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='wheel']/text()"
DESC_QUERY="/resources/resource[@id='$XMLIDQUERY'][@type='description']/text()"

path=$(basename $FILE)
slug=${path%.*}
title=$(xmllint --xpath "$TITLE_QUERY" "$DBXML")
platform=$(xmllint --xpath "$PLATFORM_QUERY" "$DBXML")

developer=$(xmllint --xpath "$DEVELOPER_QUERY" "$DBXML")
publisher=$(xmllint --xpath "$PUBLISHER_QUERY" "$DBXML")
players=$(xmllint --xpath "$PLAYERS_QUERY" "$DBXML")
ages=$(xmllint --xpath "$AGES_QUERY" "$DBXML")
tags=$(xmllint --xpath "$TAGS_QUERY" "$DBXML")
release_date=$(xmllint --xpath "$RELEASEDATE_QUERY" "$DBXML")
release_year=${release_date:0:4}
boxart=$(xmllint --xpath "$COVER_QUERY" "$DBXML")
screenshot=$(xmllint --xpath "$SCREENSHOT_QUERY" "$DBXML")
title_image=$(xmllint --xpath "$WHEEL_QUERY" "$DBXML")
description=$(xmllint --xpath "$DESC_QUERY" "$DBXML")

ASSETDIR="$CACHEDIR/assets/$slug"
ASSETDATA="$APPFILES/skyscraper/cache/$PLATFORM_SLUG"

mkdir -p $ASSETDIR

cp -v $ASSETDATA/$boxart $ASSETDIR/$slug-boxart.jpg
cp -v $ASSETDATA/$screenshot $ASSETDIR/$slug-screenshot.jpg
cp -v $ASSETDATA/$title_image $ASSETDIR/$slug-title.jpg
cp -v $APPFILES/skyscraper/media/$PLATFORM_SLUG/screenshots/$slug.png $ASSETDIR/$slug-display.png


echo "
ages: $ages
boxart: $boxart
developer: $developer
path: $path
platform: $platform
platform_slug: $PLATFORM_SLUG
players: $players
publisher: $publisher
release_date: $release_year
screenshot: $screenshot
slug: $slug
tags: $tags
title: $title
title_image: $title_image
" >$ASSETDIR/ss-$slug-details.txt

echo "$description" >$ASSETDIR/ss-$slug-description.txt

echo "
Variables:
----------

ID: $XMLIDQUERY
QUICKIDXML: $QUICKIDXML
APPFILES: $APPFILES
ASSETDIR: $ASSETDIR
ASSETDATA: $ASSETDATA
PLATFORMDIR: $PLATFORMDIR
"

echo "
Details:
--------
"

cat $ASSETDIR/ss-$slug-details.txt

echo "
Description:
------------
"

cat $ASSETDIR/ss-$slug-description.txt

#firefox "$LOCALURL/game/scrape/?path=$path&title=$title&sort_title=$sort_title&developer=$developer&publisher=$publisher&release_date=$release_year&path=$path&description=$description" &