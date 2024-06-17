#! /bin/bash

UTILS="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $UTILS/utils.sh

BACKUPDIR=$APPDIR/docs/backup

## Pull db/media from server
pull(){
	cd $CMSDIR
	/usr/bin/tar cvzf $BACKUPDIR/db/db-$(/usr/bin/date +%Y.%m%d.%H%M).tar.gz db.sqlite3
	/usr/bin/rsync -hirt brinstar:$APPDB $APPDB
	/usr/bin/rsync -hirt --progress brinstar:$CMSDIR/media/ $CMSDIR/media/
	cp $APPDB $CMSDIR/test.sqlite3
	cp $APPDB $CMSDIR/empr.db
}

## Push db/media to server
push(){
	cd $CMSDIR
	/usr/bin/tar cvzf $BACKUPDIR/db/db-$(/usr/bin/date +%Y.%m%d.%H%M).tar.gz db.sqlite3
	/usr/bin/rsync $APPDB -hirt brinstar:$APPDB
	/usr/bin/rsync -hirt --delete-before --exclude .dtrash --progress $CMSDIR/media/ brinstar:$CMSDIR/media/	
}

## Pull from repository and migrate
update-src(){
	cd $CMSDIR
	git pull origin
	. $VENV/bin/activate
	python3 -m pip install -r requirements.txt
	python3 manage.py makemigrations
	python3 manage.py migrate
}

## Update server
update-server(){
	update-src
	cd $CMSDIR
	. $VENV/bin/activate
	python3 manage.py collectstatic --noinput
	sudo service apache2 restart
	#sudo service gunicorn restart
}



help(){
	echo -e "
	Empr CLI Apps
	
	Options
	-------
	
	update-local:	Pull db/media from server
	update-src:		Update source code
	update-server:	Update source code (server)
	"
}

$1

if [[ -z $1 ]]; then
	help
fi