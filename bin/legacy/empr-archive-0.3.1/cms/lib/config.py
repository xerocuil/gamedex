import os

## Init Config class
class Config:
  app_title = "Empr"
  app_dir = os.path.dirname(os.path.realpath(__file__))
  user_dir = os.path.join(os.path.expanduser('~'))
  dotfiles = os.path.join(user_dir, '.empr')
  pkg_dir = os.path.join(dotfiles, 'pkg')
  app_db =os.path.join(dotfiles, 'db/empr.sqlite3')
  games_dir =os.path.join(user_dir, 'Games')
  roms_dir =os.path.join(games_dir, 'roms')
  archive_dir = os.path.join(os.path.expanduser('/run/media/xerocuil/2tb/Games'))