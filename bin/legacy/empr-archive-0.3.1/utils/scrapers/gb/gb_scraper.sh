#! /bin/bash

DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SCRAPERS="$(dirname $DIR)"
UTILS="$(dirname $SCRAPERS)"
source $UTILS/utils.sh

echo "$UTILS"

# Variables
#############

## Input
file="$1"
path=$(basename $file)
filename=${path##*/}
slug=${filename%.*}

## Directories
app_directory=$APPDIR
config_files=$APPFILES
cache_dir="$config_files/cache"
asset_dir="$cache_dir/assets/$slug"
scraper_dir="$app_directory/utils/scrapers/gb"

gb_json_file="$cache_dir/gb/gb_$slug.json"
gb_json_search_file="$cache_dir/gb/gb_search-$slug.json"

## Images
asset_icon=$asset_dir/gb_$slug-icon.png
asset_boxart=$asset_dir/gb_$slug-boxart.jpg
asset_background=$asset_dir/gb_$slug-background.jpg

## API
gb_api=56990bb9836a296be511b22236a52a6c6aca5dda

## Create directories
mkdir -p $asset_dir $cache_dir/gb

## Create JSON file of search results if one does not exists
if [[ ! -f $gb_json_search_file ]]; then
	curl -o $gb_json_search_file "https://www.giantbomb.com/api/search/?api_key=$gb_api&format=json&query='$slug'&resources=game&resource_type&field_list=deck,guid,name,original_release_date,platforms"
fi

### Get number of results
total_results=$(jq -r '.results[] | length' $gb_json_search_file | head -1)
total_results_cap=$(($total_results-1))

# search_results_json="$(cat $gb_json_search_file | jq '.results[] | {guid: .guid, name: .name, release_date: .original_release_date, deck: .deck}')"

# ### Get search result fields
# IFS=$'\n'

# guidlist=$(cat $gb_json_search_file | jq -r .results[].guid)

for result in $(seq 0 $total_results_cap);
do
	result_guid=$(cat $gb_json_search_file | jq -r ".results[$result].guid")
	result_name=$(cat $gb_json_search_file | jq -r ".results[$result].name")
	result_date=$(cat $gb_json_search_file | jq -r ".results[$result].original_release_date")

	echo "$result_guid	$result_name 	$result_date"
done


read -p "Enter GiantBomb GUID: " guid

if [[ -z $guid ]]; then
	exit
else
	echo "GUID: $guid"
fi

if [[ ! -f $gb_json_file ]]; then
	curl "https://www.giantbomb.com/api/game/$guid/?api_key=$gb_api&format=json&field_list=deck,developers,franchises,image,genres,name,original_game_rating,original_release_date,publishers,themes" | jq . >$gb_json_file
fi

### Set delimiter to carriage return for JSON values.
IFS=$'\n'


# Game Data

title=$(cat $gb_json_file | jq -r '.results.name')

if [[ $title == A\ * ]]; then
	sort_title="$(echo $title | cut -d " " -f 2-), A"
elif [[ $title == The\ * ]]; then
	sort_title="$(echo $title | cut -d " " -f 2-), The"
else
	sort_title="$title"
fi

description=$(cat $gb_json_file |jq -r '.results.deck')

developer_array=$(cat $gb_json_file |jq -r '.results.developers[].name')
developers=()
for dev in $developer_array; do developers+=($dev); done
developer=${developers[0]}

publisher_array=$(cat $gb_json_file |jq -r '.results.developers[].name')
publishers=()
for pub in $publisher_array; do publishers+=($pub); done
publisher=${publishers[0]}

esrb=$(cat $gb_json_file | jq -r '.results.original_game_rating[].name'|cut -d ' ' -f 2|head -n 1)

genre_array=$(cat $gb_json_file |jq -r '.results.genres[].name')
tag_array=$(cat $gb_json_file |jq -r '.results.themes[].name')
tags=()
for gb_tag in $tag_array; do tags+=($gb_tag); done
for gb_gen in $genre_array; do tags+=($gb_gen); done
tag_list=$(IFS=','; echo "${tags[*]}")

release_date=$(cat $gb_json_file |jq -r '.results.original_release_date')

# Images

## Boxart
boxart_url=$(cat $gb_json_file |jq -r '.results.image.original_url')
wget -O $asset_boxart $boxart_url

## Icon
icon_url=$(cat $gb_json_file |jq -r '.results.image.thumb_url')
wget -O $asset_icon $icon_url


echo "
###############
### Testing ###
###############

app_directory: $app_directory
asset_dir: $asset_dir
cache_dir: $cache_dir
scraper_dir: $scraper_dir
path: $path
slug: $slug

boxart_url: $boxart_url

asset_icon: $asset_icon
asset_boxart: $asset_boxart
asset_background: $asset_background

total_results: $total_results
total_results_cap: $total_results_cap

###############
"

echo "
developer: $developer
esrb: $esrb
publisher: $publisher
release_date: $release_date
sort_title: $sort_title
tags: $tag_list
title: $title
" >$asset_dir/gb-$slug-details.txt

echo "$description" >$asset_dir/gb-$slug-description.txt

echo "
Details:
--------
"

cat $asset_dir/gb-$slug-details.txt

echo "
Description:
------------
"

cat $asset_dir/gb-$slug-description.txt
