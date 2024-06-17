#! /bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRAPERS="$(dirname $DIR)"
UTILS="$(dirname $SCRAPERS)"
source $UTILS/utils.sh

HELPERS=$DIR/helpers

## Set variables
file="$1"
path=$(basename $file)
slug=$(echo $path | cut -d "." -f 1)
tgdb_apikey=fc021a8b97fe3d3e5977d7d403f1ca6cc50148ee4bbae951a47296eeb6970183
tgdb_apiurl="https://api.thegamesdb.net"

json_dir="$CACHEDIR/tgdb/json"
json_file="$json_dir/$slug.json" 
json_search_file="$json_dir/search_$slug.json"
tgdb_file="$json_dir/tgdb_$slug.json"
tgdb_search_file="$json_dir/tgdb_search_$slug.json"
tgdb_image_file="$json_dir/tgdb_image_$slug.json"

developer_list=$HELPERS/developers.json
genre_list=$HELPERS/genres.json
platform_list=$HELPERS/platforms.json
publisher_list=$HELPERS/publishers.json

mkdir -p $json_dir

## Search for TGDB ID
#####################

if [[ ! -f $tgdb_search_file ]]; then
	curl -o $tgdb_search_file "$tgdb_apiurl/v1.1/Games/ByGameName?apikey=$tgdb_apikey&name='$slug'&fields='genres,platform,release_date'"
fi

### Get remaining API allowance
echo -e "\n ### API Allowance
API calls left: $(cat $tgdb_search_file | jq .remaining_monthly_allowance)"
allowance_refresh_timer=$(cat $tgdb_search_file | jq .allowance_refresh_timer)
refresh_days=$(($allowance_refresh_timer/60/60/24))
echo -e "Days until refresh: $refresh_days\n"

### Get number of results
tgdb_total_results=$(cat $tgdb_search_file | jq .data.count)
tgdb_total_results_cap=$(($tgdb_total_results-1))

### Show HR field data
search_results_json="$(cat $tgdb_search_file | jq '.data.games[] | {game_title: .game_title, release_date: .release_date, platform: .platform, tgdb_id: .id}')"

### Get search result fields
IFS=$'\n'

echo -e "tgdb_result_array\n"
>$CACHEDIR/tgdb/search_results.txt
for tgdb_result in $(seq 0 $tgdb_total_results_cap);
do
	tgdb_result_name=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].game_title")
	tgdb_result_release_date=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].release_date")
	tgdb_result_platform_id=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].platform")
	platform_name=$(cat $platform_list | jq -r ". | select(.id==$tgdb_result_platform_id).name")
	tgdb_result_id=$(cat $tgdb_search_file | jq -r ".data.games[$tgdb_result].id")
	echo "$tgdb_result_id: $tgdb_result_name, $platform_name, $tgdb_result_release_date"
done

read -p "enter TGDB ID: " tgdb_id

echo "tgdb_id: $tgdb_id"

### If no TGDB ID is entered, the program will exit
if [[ -z $tgdb_id ]]; then rm $json_dir/*; exit; fi

### Get JSON data with TGDB ID
if [[ ! -f $tgdb_file ]]; then
	curl -o $tgdb_file "$tgdb_apiurl/v1/Games/ByGameID?apikey=$tgdb_apikey&id=$tgdb_id&fields=players,publishers,genres,overview,rating,platform,coop,os,processor,ram,hdd,video,sound,alternates"
fi


## Scrape TGDB with selected GUID
#################################

### Set delimiter to carriage return for JSON values.
IFS=$'\n'

coop=$(cat $tgdb_file | jq -r '.data.games[].coop')
description=$(cat $tgdb_file | jq -r '.data.games[].overview')

developer_id_array=()
developer_name_array=()
developer_id_array=$(cat $tgdb_file | jq -r '.data.games[].developers[]')
for dev_id in $developer_id_array
do
	developer_name=$(cat $developer_list | jq -r ". | select(.id==$dev_id).name")
	developer_name_array+=($developer_name)
done

genre_id_array=()
genre_name_array=()
genre_id_array=$(cat $tgdb_file | jq -r '.data.games[].genres[]')
for genre_id in $genre_id_array
do
	genre_name=$(cat $genre_list | jq -r ". | select(.id==$genre_id).name")
	genre_name_array+=($genre_name)
done

### Get platform
platform_id=$(cat $tgdb_file | jq -r ".data.games[].platform")
platform_name=$(cat $platform_list | jq -r ". | select(.id==$platform_id).alias")
platform_title=$(cat $platform_list | jq -r ". | select(.id==$platform_id).name")
players=$(cat $tgdb_file | jq -r ".data.games[].players")

### Get publisher
publisher_id_array=()
publisher_name_array=()
publisher_id_array=$(cat $tgdb_file | jq -r '.data.games[].publishers[]')
for pub_id in $publisher_id_array
do
	publisher_name=$(cat $publisher_list | jq -r ". | select(.id==$pub_id).name")
	publisher_name_array+=($publisher_name)
done

### Get release
release_date=$(cat $tgdb_file | jq -r ".data.games[].release_date")
rating=$(cat $tgdb_file | jq -r ".data.games[].rating"| cut -d ' ' -f 1)
title=$(cat $tgdb_file | jq -r '.data.games[].game_title')

### Get sort title
if [[ $title == A\ * ]]; then
	sort_title="$(echo $title | cut -d " " -f 2-), A"
elif [[ $title == The\ * ]]; then
	sort_title="$(echo $title | cut -d " " -f 2-), The"
else
	sort_title="$title"
fi

### Get images
asset_dir="$CACHEDIR/assets/$slug"
asset_boxart=$asset_dir/tgdb-$slug-boxart.jpg
asset_background=$asset_dir/tgdb-$slug-fanart.jpg
asset_screenshot=$asset_dir/tgdb-$slug-screenshot.jpg
asset_clearlogo=$asset_dir/tgdb-$slug-logo.png
mkdir -p $asset_dir

if [[ ! -f $tgdb_image_file ]]; then
	curl -o $tgdb_image_file "$tgdb_apiurl/v1/Games/Images?apikey=$tgdb_apikey&games_id=$tgdb_id"
fi

base_url=$(cat $tgdb_image_file | jq -r ".data.base_url.original")

#### Boxart
boxart_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.side == "front").filename')
boxart_file_base=$(basename $boxart_file | cut -d '.' -f 1)
boxart_file_ext=$(basename $boxart_file | cut -d '.' -f 2)
if [[ ! -f $asset_boxart ]]; then
	echo "No Boxart"
	wget -O $asset_boxart $base_url$boxart_file
fi

#### Background
background_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.type == "fanart").filename' | sed '1q;d')
background_file_base=$(basename $background_file | cut -d '.' -f 1)
background_file_ext=$(basename $background_file | cut -d '.' -f 2)
if [[ ! -f $asset_background ]]; then
	echo "No background"
	wget -O $asset_background $base_url$background_file
fi

#### Screenshot
screenshot_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.type == "screenshot").filename' | sed '1q;d')
screenshot_file_base=$(basename $screenshot_file | cut -d '.' -f 1)
screenshot_file_ext=$(basename $screenshot_file | cut -d '.' -f 2)
if [[ ! -f $asset_screenshot ]]; then
	echo "No screenshot"
	wget -O $asset_screenshot $base_url$screenshot_file
fi

#### Logo
logo_file=$(cat $tgdb_image_file | jq -r '.data.images[][] | select(.type == "clearlogo").filename' | sed '1q;d')
logo_file_base=$(basename $logo_file | cut -d '.' -f 1)
logo_file_ext=$(basename $logo_file | cut -d '.' -f 2)
if [[ ! -f $asset_clearlogo ]]; then
	echo "No logo"
	wget -O $asset_clearlogo $base_url$logo_file
fi

echo "
developer: $developer_name_array
genre: $genre
path: $path
publisher: $publisher_name_array
release_date: $release_date
slug: $slug
sort_title: $sort_title
title: $title
" >$asset_dir/tgdb-$slug-details.txt

echo "$description" >$asset_dir/tgdb-$slug-description.txt

echo "
Details:
--------
"
cat $asset_dir/tgdb-$slug-details.txt

echo "
Description:
------------
"
cat $asset_dir/tgdb-$slug-description.txt
