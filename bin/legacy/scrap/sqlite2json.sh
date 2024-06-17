#!/bin/bash

source $HOME/.config/empr/config.sh

EXPORTDIR="$APPDIR/docs/export/json"
mkdir -p $EXPORTDIR

echo -e "
## DEBUGGING
------------
APPDB: $APPDB
APPDIR: $APPDIR
CACHEDIR: $CACHEDIR
SQLITE: $SQLITE
UTILSDIR: $UTILSDIR
EXPORTDIR: $EXPORTDIR
"

cd $EXPORTDIR

sqlite3 $APPDB <<EOF
.headers on
.mode json
.once games.json
select * from games_game order by sort_title;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode json
.once genres.json
select * from games_genre order by name;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode json
.once platforms.json
select * from games_platform order by name;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode json
.once game_tags.json
select * from games_game_tags;
.exit
EOF

sqlite3 $APPDB <<EOF
.headers on
.mode json
.once tags.json
select * from games_tag;
.exit
EOF