#!/usr/bin/env python

import json
import os
import pprint
import requests
import sqlite3
import subprocess
import sys
import shutil

import pandas as pd

# from bs4 import BeautifulSoup
# from ftplib import FTP
# from icecream import ic
# from lib.config import Config

platform = sys.argv[1]
a405v_path = '/run/media/xerocuil/games'
platform_path = os.path.join(a405v_path, platform)
# games_json = json.load(open('/home/xerocuil/.empr/json/library/games.json'))
games_df = pd.read_json('/home/xerocuil/.empr/json/library/games.json')
platforms_df = pd.read_json('/home/xerocuil/.empr/json/library/platforms.json')
gamelist_data = []
gamelist_path = os.path.join(platform_path, 'gamelist.xml')
media_dir = '/home/xerocuil/.empr/media/games'


def convert_name(filename):
    s = filename.split('.')[0]
    s = s.replace("-", " ")
    s = s.title()
    return s


if not os.path.isdir(platform_path):
    print('Platform (' + platform + ') not found on device.')
    exit()

for f in os.listdir(platform_path):
    if f != 'images':
        if not f.endswith('.xml') and not f.endswith('.discs'):
            slug = f.split('.')[0]
            try:
                game_title = games_df.\
                loc[games_df['filename'] == f]['title'].values[0]
                game_platform_id = games_df.\
                loc[games_df['filename'] == f]['platform_id'].values[0]
                game_platform = platforms_df.\
                loc[platforms_df['id'] == game_platform_id]['slug'].values[0]
            except IndexError:
                print(f + ' not found in games.json.')
                game_title = convert_name(f)
                game_platform = ''

            gamelist_data.append({
                "path": './' + f,
                "name": game_title,
                "image": './images/' + slug + '.jpg'})

            image_dir = os.path.join(platform_path, 'images')
            if not os.path.isdir(image_dir):
                os.mkdir(image_dir)

            image_src = os.path.join(media_dir, game_platform+'/boxart/'+slug+'.jpg')
            image_dest = os.path.join(image_dir, slug+'.jpg')
            if os.path.exists(image_src):
                shutil.copyfile(image_src, image_dest)

gamelist_df = pd.DataFrame(gamelist_data)
gamelist_df.to_xml(gamelist_path, index=False, root_name='gameList', row_name="game")