#! /bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRAPERS="$(dirname $DIR)"
UTILS="$(dirname $SCRAPERS)"
source $UTILS/utils.sh

FILE=$1
FILEPATH=$(readlink -f "$FILE")
PLATFORMDIR="$(dirname $FILE)"
PLATFORM_SLUG=$(basename $PLATFORMDIR)

MEDIADIR=$CMSDIR/media
SSCACHE=$APPFILES/skyscraper/cache
SSIMPORT=$APPFILES/skyscraper/import
SSMEDIA=$APPFILES/skyscraper/media

QUICKIDXML=$SSCACHE/$PLATFORM_SLUG/quickid.xml
DBXML=$SSCACHE/$PLATFORM_SLUG/db.xml

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

ages=$(xmllint --xpath "$AGES_QUERY" "$DBXML")
boxart=$(xmllint --xpath "$COVER_QUERY" "$DBXML")
description=$(xmllint --xpath "$DESC_QUERY" "$DBXML")
developer=$(xmllint --xpath "$DEVELOPER_QUERY" "$DBXML")
players=$(xmllint --xpath "$PLAYERS_QUERY" "$DBXML")
publisher=$(xmllint --xpath "$PUBLISHER_QUERY" "$DBXML")
releasedate=$(xmllint --xpath "$RELEASEDATE_QUERY" "$DBXML")
screenshot=$(xmllint --xpath "$SCREENSHOT_QUERY" "$DBXML")
tags=$(xmllint --xpath "$TAGS_QUERY" "$DBXML")
title_image=$(xmllint --xpath "$WHEEL_QUERY" "$DBXML")

ASSETDIR="$SSIMPORT/$PLATFORM_SLUG"
ASSETDATA="$SSCACHE/$PLATFORM_SLUG"

mkdir -p $ASSETDIR/covers $ASSETDIR/screenshots $ASSETDIR/wheels

COVER=$ASSETDIR/covers/$slug.jpg
SCREENSHOT=$ASSETDIR/screenshots/$slug.jpg
WHEEL=$ASSETDIR/wheels/$slug.png

if [[ ! -f  $COVER ]]; then
	cp -v $ASSETDATA/$boxart $COVER
fi

if [[ ! -f  $SCREENSHOT ]]; then
	cp -v $ASSETDATA/$screenshot $SCREENSHOT
fi

if [[ ! -f  $WHEEL ]]; then
	cp -v $ASSETDATA/$title_image $WHEEL
fi

browser(){
	export DISPLAY=:0
	firefox "http://empr.brinstar/admin/games/game/add/?path=$path&title=$title&sort_title=$title&developer=$developer&platform=$PLATFORMID&publisher=$publisher&release_date=$releasedate&description=$description" &
}

game_id_query(){
	ssh brinstar "sqlite3 $APPDB \"select id from games_game where path = '$path';\""
}

platform_id_query(){
	ssh brinstar "sqlite3 $APPDB \"select id from games_platform where slug = '$PLATFORM_SLUG';\""
}

GAMEID=$(game_id_query)
PLATFORMID=$(platform_id_query)

if [[ -z $GAMEID ]]; then
	echo "
	DB Info:
	--------
	GAMEID:        $GAMEID
	PLATFORMID:    $PLATFORMID
	path:          $path
	platform:      $platform
	platform_slug: $PLATFORM_SLUG
	slug:          $slug

	Images:
	-------
	boxart: $boxart
	screenshot: $screenshot
	title_image: $title_image

	Details:
	--------
	title: $title
	ages: $ages
	developer: $developer
	players: $players
	publisher: $publisher
	releasedate: $releasedate
	tags: $tags

	Description:
	------------
	$description
	"

	browser
else
	echo "Game is already in the database."
fi

echo -e "\nWould you like to add the images to the database? [y/n]\n"

read IMGUPLOAD

if [[ ${IMGUPLOAD,,} = "y" ]]; then
	GAMEID=$(game_id_query)
	DISPLAY=$SSMEDIA/$PLATFORM_SLUG/screenshots/$slug.png

	if [[ $PLATFORM_SLUG = "ps1" ]]; then
		SYSTEM_SLUG="psx"
	elif [[ $PLATFORM_SLUG = "gamecube" ]]; then
		SYSTEM_SLUG="gc"
	else
		SYSTEM_SLUG=$PLATFORM_SLUG
	fi

	if [[ ! -z $GAMEID ]]; then
		skyscraper -p $SYSTEM_SLUG -s import $FILE
		skyscraper -p $SYSTEM_SLUG $FILE

		if [[ -f $COVER ]]; then
			echo "cover: $COVER"
			scp $COVER brinstar:$MEDIADIR/games/boxart/
			ssh brinstar "sqlite3 $APPDB \"update games_game set boxart = 'games/boxart/$slug.jpg' where id = $GAMEID ;\""
		fi

		if [[ -f $SCREENSHOT ]]; then
			echo "screenshot: $SCREENSHOT"
			scp $SCREENSHOT brinstar:$MEDIADIR/games/screenshot/
			ssh brinstar "sqlite3 $APPDB \"update games_game set screenshot = 'games/screenshot/$slug.jpg' where id = $GAMEID ;\""
		fi

		if [[ -f $WHEEL ]]; then
			echo "wheel: $WHEEL"
			scp $WHEEL brinstar:$MEDIADIR/games/title/
			ssh brinstar "sqlite3 $APPDB \"update games_game set title_image = 'games/title/$slug.png' where id = $GAMEID ;\""
		fi

		if [[ -f $DISPLAY ]]; then
			echo "display: $DISPLAY"
			scp $DISPLAY brinstar:$MEDIADIR/games/display/
			ssh brinstar "sqlite3 $APPDB \"update games_game set display = 'games/display/$slug.png' where id = $GAMEID ;\""
		fi
	else
		echo "Game not added to database. Exiting..."
		exit
	fi
else
	echo -e "Exiting..."
fi

# echo "
# Variables:
# ----------
# APPFILES:       $APPFILES
# ASSETDATA:      $ASSETDATA
# ASSETDIR:       $ASSETDIR
# PLATFORM_SLUG:  $PLATFORM_SLUG
# PLATFORMDIR:    $PLATFORMDIR
# QUICKIDXML:     $QUICKIDXML
# XMLIDQUERYID:   $XMLIDQUERY
# "







