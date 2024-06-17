#! /bin/bash

UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APPDIR="$(dirname $UTILS)"
source $UTILS/utils.sh

PLATFORMS=($(sqlite3 "$APPDB" "select slug from games_platform";))
MEDIADIR="$APPFILES/media"
COLLECTIONSDIR="$HOME/.emulationstation/collections"

generate_xml(){
  echo -e "<?xml version=\"1.0\"?>\n<gameList>" >$ESGAMELISTDIR/gamelist.xml

  for g in $GAMES
  do
    ID_QUERY=$(sqlite3 "$APPDB" "select id from games_game where path = '$g'";)
    TITLE_QUERY=$(sqlite3 "$APPDB" "select title from games_game where id = '$ID_QUERY'";)
    DESC_QUERY=$(sqlite3 "$APPDB" "select description from games_game where id = '$ID_QUERY'";)
    DEV_QUERY=$(sqlite3 "$APPDB" "select developer from games_game where id = '$ID_QUERY'";)
    PUB_QUERY=$(sqlite3 "$APPDB" "select publisher from games_game where id = '$ID_QUERY'";)
    ESRB_QUERY=$(sqlite3 "$APPDB" "select esrb from games_game where id = '$ID_QUERY'";)
    GENREID_QUERY=$(sqlite3 "$APPDB" "select genre_id from games_game where id = '$ID_QUERY'";)
    GENRE_QUERY=$(sqlite3 "$APPDB" "select name from games_genre where id = '$GENREID_QUERY'";)
    RELEASEDATE_QUERY=$(sqlite3 "$APPDB" "select release_date from games_game where id = '$ID_QUERY'";)
    PLAYER_QUERY=$(sqlite3 "$APPDB" "select player from games_game where id = '$ID_QUERY'";)

    IFS=$'\n'
    TAGID_QUERY=($(sqlite3 "$APPDB" "select tag_id from games_game_tags where game_id = '$ID_QUERY'";))
    TAGARRAY=()
    for TAGID in "${TAGID_QUERY[@]}"
    do
      TAGS=$(sqlite3 "$APPDB" "select name from games_tag where id = '$TAGID';")
      TAGARRAY+=($TAGS)
    done

    DISPLAY_QUERY=$(sqlite3 "$APPDB" "select display from games_game where id = '$ID_QUERY'";)
    BOXART_QUERY=$(sqlite3 "$APPDB" "select boxart from games_game where id = '$ID_QUERY'";)

    if [[ -z $DISPLAY_QUERY ]]; then
      IMAGE="$BOXART_QUERY"
    else
      IMAGE="$DISPLAY_QUERY"
    fi

    if [[ ! -z $TITLE_QUERY ]]; then
      echo -e " <game>
    <path>./$g</path>
    <name>$TITLE_QUERY</name>
    <desc>$DESC_QUERY</desc>
    <developer>$DEV_QUERY</developer>
    <publisher>$PUB_QUERY</publisher>
    <esrb>$ESRB_QUERY</esrb>
    <genre>$GENRE_QUERY</genre>
    <releasedate>$RELEASEDATE_QUERY</releasedate>
    <players>$PLAYER_QUERY</players>
    <image>$MEDIADIR/$IMAGE</image>
  </game>" >>"$ESGAMELISTDIR/gamelist.xml"
    fi
  done

  echo -e "</gameList>" >>"$ESGAMELISTDIR/gamelist.xml"

  echo -e "<theme>
  <formatVersion>4</formatVersion>
  <include>./../empr.xml</include>

  <view name=\"system\">
    <image name=\"logo\">
      <path>./system.svg</path>
    </image>
  </view>

  <view name=\"basic, detailed, video\">
    <image name=\"logo\">
      <path>./system.svg</path>
      <pos>0.266 0.074</pos>
      <maxSize>0.460 0.126</maxSize>
      <origin>0.5 0.5</origin>
    </image>
  </view>

  <view name=\"basic\">   
  </view>

  <view name=\"detailed\">
  </view>
</theme>" >"$ESTHEME/theme.xml"
}

generate_collections(){
  echo -e "\nGenerating collections...\n"
  COLLECTION_QUERY=$(sqlite3 "$APPDB" "select id,name from games_collection order by name;")
  IFS=$'\n'
  for c in $COLLECTION_QUERY
  do
    COLLECTION_ID=$(echo "$c" | cut -d "|" -f 1)
    COLLECTION_NAME=$(echo "$c" | cut -d "|" -f 2)
    COLLECTION_SLUG=$(echo $COLLECTION_NAME | iconv -t ascii//TRANSLIT | sed -r s/[^a-zA-Z0-9\'\&\ ]+/-/g | sed -r s/^-+\|-+$//g)
    GAME_QUERY=$(sqlite3 "$APPDB" "select path,platform_id,release_date from games_game where collection_id = $COLLECTION_ID order by release_date asc;")
    CONFIG_FILE="$COLLECTIONSDIR/custom-$COLLECTION_SLUG.cfg"
    rm -f "$CONFIG_FILE"
    
    for g in $GAME_QUERY
    do
      GAME_PATH=$(echo "$g" | cut -d "|" -f 1)
      GAME_PLATFORM=$(echo "$g" | cut -d "|" -f 2)
      PLATFORM_QUERY=$(sqlite3 "$APPDB" "select slug from games_platform where id = $GAME_PLATFORM;")
      GAME_LOC="$GAMESDIR/roms/$PLATFORM_QUERY/$GAME_PATH"

      if [[ -f $GAME_LOC ]]; then
        echo -e "$GAME_LOC" >>"$CONFIG_FILE"
      fi
    done
  done

  GENRE_QUERY=$(sqlite3 "$APPDB" "select id,name from games_genre order by name;")
  for g in $GENRE_QUERY
  do
    GENRE_ID=$(echo "$g" | cut -d "|" -f 1)
    GENRE_NAME=$(echo "$g" | cut -d "|" -f 2)
    GENRE_SLUG=$(echo "$GENRE_NAME" | iconv -t ascii//TRANSLIT | sed -r s/[^a-zA-Z0-9\'\&\ ]+/-/g | sed -r s/^-+\|-+$//g)
    GAME_GENRE_QUERY=$(sqlite3 "$APPDB" "select platform_id,path,release_date from games_game where genre_id = $GENRE_ID order by release_date asc;")
    GENRE_CONFIG_FILE="$COLLECTIONSDIR/custom-$GENRE_SLUG Games.cfg"
    rm -f "$GENRE_CONFIG_FILE"

    for game in $GAME_GENRE_QUERY
    do
      GAME_GENRE_PATH=$(echo "$game" | cut -d "|" -f 2)
      GAME_GENRE_PLATFORM=$(echo "$game" | cut -d "|" -f 1)
      GENRE_PLATFORM_QUERY=$(sqlite3 "$APPDB" "select slug from games_platform where id = $GAME_GENRE_PLATFORM;")
      GENRE_GAME_LOC="$GAMESDIR/roms/$GENRE_PLATFORM_QUERY/$GAME_GENRE_PATH"

      if [[ -f $GENRE_GAME_LOC ]]; then
        echo -e "$GENRE_GAME_LOC" >>"$GENRE_CONFIG_FILE"
      fi
    done
  done
}

echo -e "\nGenerating xml files...\n"
for PLATFORM in ${PLATFORMS[*]}
do
  PLATFORMDIR="$ROMSDIR/$PLATFORM"
  ESGAMELISTDIR="$HOME/.emulationstation/gamelists/$PLATFORM"
  ESTHEME="$HOME/.emulationstation/themes/empr/$PLATFORM"

  if [[ -d $PLATFORMDIR ]]; then
    GAMES=$(ls -1 $PLATFORMDIR)
  fi

  if [[ -d $PLATFORMDIR ]]; then
    mkdir -p $ESGAMELISTDIR $ESTHEME
    generate_xml "$PLATFORM"
  fi
done

generate_collections
