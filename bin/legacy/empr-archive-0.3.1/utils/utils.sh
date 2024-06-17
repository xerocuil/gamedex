#! /bin/bash

# Global Variables

## Application name/slug
APPTITLE="Empr"
APPSLUG=$(echo $APPTITLE | sed -e 's/ /-/g' | awk '{print tolower($0)}')

## Global directories
UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
APPDIR="$(dirname $UTILS)"
BUILD=$APPDIR/build
CMS="$APPDIR/cms"
DIST=$APPDIR/dist
VENV="$HOME/.python-env/empr"

APPFILES="$HOME/.empr"
CACHEDIR="$APPFILES/cache"
PHOTODB=$APPFILES/digikam

APPDB="$APPFILES/db/empr.sqlite3"
LOCALURL="127.0.0.1:8088"

## Game Settings
GAMESDIR="$HOME/Games"
PCDIR="$GAMESDIR/pc"
ROMSDIR="$GAMESDIR/roms"
ARCHIVEDIR="/run/media/$USER/2tb/Games"
CORES=$HOME/.config/retroarch/cores

## System Settings
SQLITE="/usr/bin/sqlite3"


# Modules
source $UTILS/git.sh
source $UTILS/help.sh
source $UTILS/report.sh
source $UTILS/django.sh
# source $UTILS/empr.sh


# Functions

## List functions
utils.list(){
  array=()
  for i in $(ls -1 $UTILS/*.sh); do
    getFunctions="$(grep -e "(){" $i | grep -v -e "#" -e "_" -e "utils.list" | sort)"
    
    for i in $getFunctions; do
      
      item="${i%(*}"
      array+=($item)
    done
  done

  IFS=$'\n' sorted=($(sort <<<"${array[*]}")); unset IFS
  
  printf "\n  %s\n\n" "utils functions"
  n=0
  for i in "${sorted[@]}"; do
    n=$(($n+1))
    printf "%3d | %s\n" "$n" "$i"
  done
  printf "\n"
}

echo -e "\nUtils loaded\nRun utils.help for more info\n"
