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
JSON_DIR = os.path.join(APP_DIR, 'import/json')
COLLECTIONS_JSON = os.path.join(JSON_DIR, 'collections.json')
GAMES_JSON = os.path.join(JSON_DIR, 'games.json')
GENRES_JSON = os.path.join(JSON_DIR, 'genres.json')
PLATFORMS_JSON = os.path.join(JSON_DIR, 'platforms.json')
TAGS_JSON = os.path.join(JSON_DIR, 'tags.json')
GAME_TAGS_JSON = os.path.join(JSON_DIR, 'game_tags.json')

try:
    CONNECTION = sqlite3.connect(Config.DB)
    CURSOR = CONNECTION.cursor()
except sqlite3.OperationalError as e:
    ic('Could not find database.')
    exit()

## IMPORT LEGACY DATA ##
def import_collections():
    collections = json.load(open(COLLECTIONS_JSON))
    collection_columns = ['id','name','description']

    for row in collections:
        keys= tuple(row[c] for c in collection_columns)
        try:
            CURSOR.execute('insert into collection values(?,?,?)',keys)
            print(f'{row["name"]} data inserted successfully.')
        except sqlite3.IntegrityError:
            print(f'{row["name"]} already in database.')

    CONNECTION.commit()


def import_genres():
    genres = json.load(open(GENRES_JSON))
    genre_columns = ['id','name','legacy_id']
    for row in genres:
        keys= tuple(row[c] for c in genre_columns)
        try:
            CURSOR.execute('insert into genre values(?,?,?)',keys)
            print(f'{row["name"]} data inserted successfully.')
        except sqlite3.IntegrityError:
            print(f'{row["name"]} already in database.')

    CONNECTION.commit()


def import_platforms():
    platforms = json.load(open(PLATFORMS_JSON))
    platform_columns = ['id', 'emulator', 'launcher', 'name', 'ra_core', 'slug', 'legacy_id']
    for row in platforms:
        keys= tuple(row[c] for c in platform_columns)

        try:
            CURSOR.execute('insert into platform values(?,?,?,?,?,?,?)',keys)
            print(f'{row["name"]} data inserted successfully.')
        except sqlite3.IntegrityError:
            print(f'{row["name"]} already in database.')

    CONNECTION.commit()


def import_games():
    games = json.load(open(GAMES_JSON))
    genres = json.load(open(GENRES_JSON))
    platforms = json.load(open(PLATFORMS_JSON))
    tags = json.load(open(TAGS_JSON))
    game_tags = json.load(open(GAME_TAGS_JSON))


    for g in games:
        g['last_played'] = None
        g['play_count'] = None
        g['players'] = int(g['players'])
        if len(g['year']) > 4:
            g['year'] = int(g['year'][:4])

        tag_array = []
        for gt in game_tags:
            if g['id'] == gt['game_id']:
                tag_id = gt['tag_id']
                for t in tags:
                    if tag_id == t['id']:
                        tag_array.append(t['name'])

        if tag_array:
            tag_string = ', '.join(tag_array)
        else:
            tag_string = None
        g['tags'] = tag_string


        
        for genre in genres:
            if g['genre_id'] == int(genre['legacy_id']):
                g['genre_id'] = int(genre['id'])
                break

        for platform in platforms:
            try:
                if g['platform_id'] == int(platform['legacy_id']):
                    g['platform_id'] = int(platform['id'])
                    break
            except ValueError:
                pass

    game_columns = [
        'id',
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
        'favorite',
        'filename',
        'genre_id',
        'gpu',
        'hdd',
        'last_played',
        'mod',
        'notes',
        'online_multiplayer',
        'operating_system',
        'platform_id',
        'play_count',
        'players',
        'processor',
        'publisher',
        'ram',
        'region',
        'save_path',
        'steam_id',
        'store',
        'tags',
        'title',
        'translation',
        'year'
    ]

    for row in games:
        keys= tuple(row[c] for c in game_columns)
        CURSOR.execute('insert into game values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',keys)
        print(f'{row["title"]} data inserted successfully.')

    CONNECTION.commit()


# Import all
def import_all():
    import_genres()
    import_platforms()
    import_collections()
    import_games()
    CONNECTION.close()



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
    
    platforms = json.load(open(PLATFORMS_JSON))

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




## CONVERT CSV TO JSON
IMPORT_DIR = os.path.join(APP_DIR, 'import')
IMPORT_JSON = os.path.join(IMPORT_DIR, 'json')

def convert_genres():
    genres_csv = os.path.join(IMPORT_DIR, 'genres.csv')
    genres_json = os.path.join(IMPORT_JSON, 'genres.json')
     
    # Init data array
    data = []

    # Open csv file in DictReader
    with open(genres_csv, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row to a dictionary and add to data
        for row in csvReader:
            row_dict = {}
            
            row_dict = {'id': row['new_id'], 'name': row['genre'], 'legacy_id': row['legacy_id']}

            ic(row_dict)
            data.append(row_dict)

    # Dump data to file
    with open(genres_json, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def convert_platforms():
    platforms_csv = os.path.join(IMPORT_DIR, 'platforms.csv')
    platforms_json = os.path.join(IMPORT_JSON, 'platforms.json')
     
    # Init data array
    data = []

    # Open csv file in DictReader
    with open(platforms_csv, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row to a dictionary and add to data
        for row in csvReader:
            row_dict = {}
            
            row_dict = {'id': row['new_id'], 'emulator': row['emulator'], 'launcher': row['launcher'], 'name': row['name'], 'ra_core': row['ra_core'], 'slug': row['slug'], 'legacy_id': row['id']}

            ic(row_dict)
            data.append(row_dict)

    # Dump data to file
    with open(platforms_json, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

def convert_all_csv():
    convert_genres()
    convert_platforms()
## END Convert CSV to JSON