#  Report

utils.report(){
  echo "
    # $APPTITLE

    ## Application Info
    
    APPTITLE:   $APPTITLE
    APPSLUG:    $APPSLUG
    VERSION:    $VERSION

    ## Global directories

    APPDIR:     $APPDIR
    UTILS:      $UTILS
    
    ## Dist. Directories

    BUILD:      $BUILD
    DIST:       $DIST
    
    ## App directories

    BROWSER:    $BROWSER
    CMS:        $CMS
    VENV:       $VENV

    APPFILES:   $APPFILES
    CACHEDIR:   $CACHEDIR

    PCDIR:      $PCDIR
    ROMSDIR:    $ROMSDIR

    APPDB:      $APPDB
    LOCALURL:   $LOCALURL
    SQLITE:     $SQLITE
  "
}