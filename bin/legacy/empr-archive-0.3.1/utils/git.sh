# Git

## Add
git.add(){
  currentDir="$(pwd)"
  cd $APPDIR
  echo -e "\nAdding files to $APPTITLE\n"
  git add -v .
  echo -e ""
  cd $currentDir
}

## Commit
git.commit(){
  message="$1"
  currentDir="$(pwd)"
  cd $APPDIR

  if [[ -z $1  ]]; then
    message="$(date +'%Y.%m%d.%H%M')"
  else
    message="$(date +'%Y.%m%d.%H%M') | $message"
  fi

  echo -e "\n[ $message ]\n\nCommit (y/n)?\n"
  read
  
  if [[ $REPLY == "y" ]]; then
    git commit -m "$message"
  fi
  
  cd "$currentDir"
}

## Log (latest 10 commits)
git.log(){
  currentDir="$(pwd)"
  cd $APPDIR
  echo -e "\nLatest 10 Commits for $APPTITLE\n"
  git log -10 --pretty='format:%<(10)%C(auto)%h %s %C(auto)%d'
  echo -e ""
  cd $currentDir
}

## Push
git.push(){
  currentDir="$(pwd)"
  cd $APPDIR
  git push origin main
  cd $currentDir
}

## Quick Save (Commit/Push)
git.qs(){
  message="$1"
  git.add
  git.commit "$message"
  # git.push
}

## Status
git.status(){
  currentDir="$(pwd)"
  cd $APPDIR
  echo -e "\n$APPTITLE\n"
  git status
  cd $currentDir
}
