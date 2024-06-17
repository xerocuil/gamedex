import os
import sys
import sqlite3
from sqlite3 import Error

USER_DIR = os.path.expanduser('~')
GAMES_DIR = os.path.join(USER_DIR,'Games')
GAMES_ARCHIVE = '/run/media/xerocuil/2tb/Games'
ROMS_DIR = os.path.join(GAMES_DIR,'roms')
PC_DIR = os.path.join(GAMES_DIR,'pc')
APPFILES = os.path.join(USER_DIR,'.empr')
EMPRDB = os.path.join(APPFILES,'db/empr.sqlite3')

# def check_archive(platform,file_name):
#   ARCHIVE_DIR = os.path.join(GAMES_ARCHIVE, '/roms/' + platform)
#   file_slug = os.path.splitext(file_name)[0]
#   file_archive_name = file_slug + '.tar.gz'
#   file_archive_path = os.path.join(ARCHIVE_DIR, file_archive_name)
#   file_path = os.path.join(ARCHIVE_DIR, file_name)
#   print("file_archive_path: " + file_archive_path)
#   print("file_path: " + file_path)
  
#   if os.path.exists(file_archive_path):
#     print("ROM archive found.")
#   elif os.path.exists(file_path):
#     print("ROM found.")
#   else:
#     print("Nothing found.")

def check_installed(platform, file_name):
  if platform == 'pc':
    GAME_PATH = os.path.join(PC_DIR,'start.sh')
  else:
    GAME_DIR = os.path.join(ROMS_DIR,platform)
    GAME_PATH = os.path.join(GAME_DIR,file_name)

  if os.path.exists(GAME_PATH):
    return True
  else:
    return False

# check_archive("lynx","battle-wheels.lnx")
print(check_installed("lynx", "battle-wheels.lnx"))
print(check_installed("genesis", "beyond-oasis.gen"))
