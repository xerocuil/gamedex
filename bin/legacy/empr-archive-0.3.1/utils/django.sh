## Check for virtual env / create if missing
check_venv(){
  if [[ ! -d $VENV ]]; then
    python3 -m venv $VENV
    source $VENV/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r $CMS/requirements.txt
  else
    source $VENV/bin/activate
  fi
}

## Django launcher
django.launcher(){
  check_venv
  $DIST/lin/$APPSLUG/$APPSLUG runserver $LOCALURL --noreload &
  $BROWSER/lin/chrome "--app=file://$CMS/games/templates/gui/loading.html --user-data-dir=$APPFILES/data --window-size=1280,720"
  django.stop
}

django.package(){
  check_venv
  python3 $CMS/manage.py makemigrations
  python3 $CMS/manage.py migrate
  python3 $CMS/manage.py collectstatic --noinput

  pyinstaller --clean  -y \
    --distpath $DIST \
    --workpath $BUILD \
    --add-data $CMS/AppRun:. \
    --add-data $CMS/empr.desktop:. \
    --add-data $CMS/empr.png:. \
    --add-data $CMS/browser/linux-x64:browser/linux-x64 \
    --add-data $CMS/games:games \
    --add-data $CMS/media:media \
    --add-data $CMS/static:static \
    --name=$APPSLUG $CMS/empr.py
}

## Django server
django.start(){
  check_venv
  python3 $CMS/manage.py runserver $LOCALURL &
}

django.stop(){
  pkill -f runserver
}

