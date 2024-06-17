#!/usr/bin/env python

import csv
import json
import os
import shutil
import sqlite3
import sys

from icecream import ic
from lib.config import Config

APP_DIR = os.path.dirname(os.path.abspath(__file__))


## IMPORT LEGACY DATA ##
def import_collections():
    JSON_DIR = os.path.join(APP_DIR, 'json')
    collections_json = os.path.join(JSON_DIR, 'collections.json')

    try:
        connection = sqlite3.connect(Config.DB)
        cursor = connection.cursor()
    except sqlite3.OperationalError as e:
        ic('Could not find database.')
        exit()

    collections = json.load(open(collections_json))
    collection_columns = ['id','name','description']

    for row in collections:
        keys= tuple(row[c] for c in collection_columns)
        cursor.execute('insert into collection values(?,?,?)',keys)
        print(f'{row["name"]} data inserted Successfully')

    connection.commit()
    connection.close()

def import_genres():
    JSON_DIR = os.path.join(APP_DIR, 'json')
    genres_json = os.path.join(JSON_DIR, 'genres.json')

    try:
        connection = sqlite3.connect(Config.DB)
        cursor = connection.cursor()
    except sqlite3.OperationalError as e:
        ic('Could not find database.')
        exit()

    genres = json.load(open(genres_json))
    genre_columns = ['id','name','legacy_id']
    for row in genres:
        keys= tuple(row[c] for c in genre_columns)
        cursor.execute('insert into genre values(?,?,?)',keys)
        print(f'{row["name"]} data inserted Successfully')

    connection.commit()
    connection.close()

def import_platforms():
    JSON_DIR = os.path.join(APP_DIR, 'json')
    platforms_json = os.path.join(JSON_DIR, 'platforms.json')

    # try:
    #     connection = sqlite3.connect(Config.DB)
    #     cursor = connection.cursor()
    # except sqlite3.OperationalError as e:
    #     ic('Could not find database.')
    #     exit()

    platforms = json.load(open(platforms_json))
    platform_columns = ['id', 'emulator', 'launcher', 'name', 'ra_core', 'slug', 'legacy_id']
    for row in platforms:
        keys= tuple(row[c] for c in platform_columns)
        cursor.execute('insert into platform values(?,?,?,?,?,?,?)',keys)
        print(f'{row["name"]} data inserted Successfully')

    connection.commit()
    connection.close()

def import_games():
    JSON_DIR = os.path.join(APP_DIR, 'import/json')
    games_json = os.path.join(JSON_DIR, 'games.json')
    genres_json = os.path.join(JSON_DIR, 'genres.json')
    platforms_json = os.path.join(JSON_DIR, 'platforms.json')

    try:
        connection = sqlite3.connect(Config.DB)
        cursor = connection.cursor()
    except sqlite3.OperationalError as e:
        ic('Could not find database.')
        exit()

    games = json.load(open(games_json))
    genres = json.load(open(genres_json))
    platforms = json.load(open(platforms_json))

    for g in games:
        # ic(g['title'], g['genre_id'], g['year'])
        if len(g['year']) > 4:
            g['year'] = int(g['year'][:4])
        # ic('new year:',g['year'])
        
        for genre in genres:
            # ic(genre['id'], genre['legacy_id'])
            if g['genre_id'] == int(genre['legacy_id']):
                g['genre_id'] = int(genre['id'])
                # ic(g['genre_id'], genre['legacy_id'], genre['name'])
                break

        for platform in platforms:
            try:
                if g['platform_id'] == int(platform['legacy_id']):
                    g['platform_id'] = int(platform['id'])
                    # ic(g['platform_id'], platform['legacy_id'], platform['name'])
                    break
            except ValueError:
                pass

    game_columns = [
        'alt_title',
        'archived',
        'co_op',
        'collection_id',
        'controller_support',
        'date_added',
        'date_modified',
        'description',
        'developer',
        'esrb',
        'filename',
        'genre_id',
        'gpu',
        'hdd',
        'id',
        'mod',
        'notes',
        'online_multiplayer',
        'operating_system',
        'platform_id',
        'players',
        'processor',
        'publisher',
        'ram',
        'region',
        'save_path',
        'steam_id',
        'store',
        'title',
        'translation',
        'year'
    ]

    for row in games:
        keys= tuple(row[c] for c in game_columns)
        cursor.execute('insert into game values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',keys)
        print(f'{row["title"]} data inserted Successfully')

    connection.commit()
    connection.close()

# Imports
# import_genres()
# import_platforms()
# import_collections()
# import_games()
## END IMPORT LEGACY DATA


## IMPORT MEDIA
MEDIA_DIR = os.path.join(Config.MEDIA, 'games')
LEGACY_MEDIA_DIR = os.path.join(os.path.expanduser('~'), '.empr_v031/media')


def get_media(slug, platform_slug, media_url):
    try:
        media_type = media_url.split('/')[1]
    except:
        media_type = None
    if media_type:
        if media_type == 'header':
            media_type = 'grid'
        if media_type == 'title':
            media_type = 'logo'
        new_dir = os.path.join(MEDIA_DIR, platform_slug+'/'+media_type)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

        legacy_media = os.path.join(LEGACY_MEDIA_DIR, media_url)
        file_ext = os.path.basename(legacy_media).split('.')[1]
        new_media = os.path.join(new_dir, slug+'.'+file_ext)

        ic(slug, media_type, legacy_media, new_media)

        try:
            shutil.copyfile(legacy_media, new_media)
        except FileNotFoundError:
            ic('File not found', legacy_media)


def import_media():
    
    platforms_json = '/home/xerocuil/Documents/projects/empr/src/import/games_platform.json'
    platforms = json.load(open(platforms_json))

    try:
        legacy_db = sqlite3.connect('/home/xerocuil/.empr_v031/db/v031.sqlite3')
        legacy_cursor = legacy_db.cursor()
        ic('Database connected.')
    except sqlite3.OperationalError as e:
        ic('Could not find database.')
        exit()
    # /home/xerocuil/.empr_v031/db/
    query = legacy_cursor.execute('select path, platform_id, boxart, display, header, icon, manual, screenshot, title_image, wallpaper from games_game where 1;')
    for q in query:
        path = q[0]
        
        platform_id =q[1]
        boxart = q[2]
        display = q[3]
        header = q[4]
        icon = q[5]
        manual = q[6]
        screenshot = q[7]
        title_image = q[8]
        wallpaper = q[9]
    
        for p in platforms:
            if p['id'] == platform_id:
                platform_slug = p['slug']
                break

        slug = path.split('.')[0]

        get_media(slug, platform_slug, boxart)
        get_media(slug, platform_slug, display)
        get_media(slug, platform_slug, header)
        get_media(slug, platform_slug, icon)
        get_media(slug, platform_slug, manual)
        get_media(slug, platform_slug, screenshot)
        get_media(slug, platform_slug, title_image)
        get_media(slug, platform_slug, wallpaper)