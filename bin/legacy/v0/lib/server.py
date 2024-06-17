#!/usr/bin/env python

import glob
import json
import os
import random
import sqlite3
import subprocess
import sys

import pandas as pd
from icecream import ic

UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(UTILS_DIR))

from lib.extensions import Config


# ARGS

try:
    CMD = sys.argv[1]
except IndexError:
    CMD = None

try:
    ARG = sys.argv[2]
except IndexError:
    ARG = None

# GLOBALS
FTP_HOST = Config.FTP_HOST
FTP_PORT = Config.FTP_PORT
FTP_PATH = Config.FTP_PATH
NFS_HOST = '/mnt/games'



## DATABASE
try:
    CONNECTION = sqlite3.connect(Config.DB)
    CURSOR = CONNECTION.cursor()
except sqlite3.OperationalError as e:
    ic('Could not find database.')
    exit()

## FUNCTIONS
    
'''List games on server that are not in the database.'''

def find_unregistered(platform_slug):
    archive_dir = os.path.join(NFS_HOST, platform_slug)
    archive_data = json.load(open(os.path.join(archive_dir, 'genesis.json')))
    archive_list = os.listdir(archive_dir)
    archive_list = sorted(archive_list)
    unregistered = []

    '''Get list of file names from JSON file'''
    archive_data_games = archive_data['games']
    archive_filename_array = []
    for a in archive_data_games:
        archive_filename_array.append(a['archive'])

    '''Select items that aren't listed in JSON file'''
    for archive in archive_list:
        if not archive in archive_filename_array:
            if archive.endswith('.zip'):
                unregistered.append(archive)

    return unregistered


# def update_archive(platform_slug):
#     platform_obj = {}
#     # local_games = os.path.join(Config.GAMES_DIR, platform_slug)
#     archive_dir = os.path.join(NFS_HOST, platform_slug)
    
#     platform_query = "SELECT id, name FROM platform where slug = '"+platform_slug+"';"

#     CURSOR.execute(platform_query)
#     platform_data = CURSOR.fetchone()

#     platform_obj.update({"id": platform_data[0], "name": platform_data[1]})


#     games_query = "SELECT id, filename, title FROM game where platform_id = '"+str(platform_data[0])+"' ORDER BY filename;"
#     CURSOR.execute(games_query)
#     games_data = CURSOR.fetchall()

#     not_in_archive = []
#     games_obj = []
#     for game in games_data:
#         game_id = game[0]
#         filename = game[1]
#         title = game[2]
#         game_slug = filename.split('.')[0]
#         game_archive_file = game_slug+'.zip'
#         game_archive_path = os.path.join(archive_dir, game_archive_file)

#         if os.path.exists(game_archive_path):
#             games_obj.append({"id": game_id, "filename": filename, "title": title, "archive":game_archive_file})
#         else:
#             not_in_archive.append(game_archive_file)
#             ic(game_archive_file)

#     if len(not_in_archive) >1:
#         ic(not_in_archive)

#     platform_obj.update({"games": games_obj})

#     json_path = os.path.join(archive_dir, platform_slug+'.json')
#     with open(json_path, 'w', encoding='utf-8') as f:
#         json.dump(platform_obj, f, indent=4)

def print_help():
    print('No commands given.')


def main():
    if CMD and ARG:
        globals()[CMD](ARG)
    elif CMD:
        globals()[CMD]()
    else:
        print_help()


if __name__ == '__main__':
    main()











# def update_server_list(platform_slug):
#     platform_dir = os.path.join(LOCAL_HOST, platform_slug)
#     archives = []
#     game_db_info = []
#     for file in os.listdir(platform_dir):
#         file_slug = file.split('.')[0]
#         ic(file_slug)
#         archives.append(file)
#         CURSOR.execute("select id, title from game where filename like '"+file_slug+".%'")
#         game = CURSOR.fetchone()
#         ic(game)

    # ic(sorted(archives))