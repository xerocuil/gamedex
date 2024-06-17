#!/usr/bin/env python

import json
import os
import shutil
import sqlite3
import subprocess
import tarfile
# from icecream import ic  # Debug
from lib.extensions import Config

try:
    CONNECTION = sqlite3.connect(Config.DB)
    CURSOR = CONNECTION.cursor()
except sqlite3.OperationalError as e:
    print('Could not find database.', e)
    exit()

EXPORT_DIR = os.path.join(Config.PROFILE_DIR, 'export')


# FUNCTIONS

def create_readme(file):
    # Local variables
    user_file_dir = os.path.dirname(file)
    readme_path = os.path.join(user_file_dir, 'readme.md')
    logo_path = os.path.join(user_file_dir, 'logo.png')
    manual_path = os.path.join(user_file_dir, 'manual.pdf')
    extras_path = os.path.join(os.path.dirname(user_file_dir), 'extras')

    # Open json file
    with open(file) as user_file:
        json_data = json.load(user_file)

    # Init data array
    l = []

    # Add logo as header
    # Use title if logo does not exist
    if os.path.exists(logo_path):
        l.append("![logo](logo.png)\n")
    else:
        l.append("# " + json_data['title'] + "\n")
        try:
            if json_data['alt_title']:
                l.append("  \nAlt Title: " + json_data['title'])
        except Exception as e:
            print(e)
            pass

    # General data
    l.append("\n## Description\n\n" + json_data['description'] + "\n")
    l.append("\n**Genre:** " + json_data['genre'])

    try:
        if json_data['tags']:
            tags = ", ".join(json_data['tags'])
            l.append("  \n**Tags:** " + tags)
    except Exception as e:
        print(e)
        pass

    l.append("  \n**Released:** " + str(json_data['year']))
    l.append("  \n**Developer:** " + str(json_data['developer']))
    l.append("  \n**Publisher:** " + str(json_data['publisher']))

    try:
        if json_data['esrb']:
            l.append("  \n**ESRB Rating:** " + json_data['esrb'])
    except:
        pass

    l.append("  \n**Player(s):** ")

    if json_data['players'] == 1:
        l.append("Single-player")
    else:
        l.append(str(json_data['players']) + " players")

    try:
        if json_data['co_op']:
            l.append(", Co-op")
    except:
        pass

    try:
        if json_data['online_multiplayer']:
            l.append(", Online Multiplayer")
    except:
        pass

    try:
        if json_data['controller_support']:
            l.append("  \n**Controller Support:** Yes  ")
    except:
        pass

    try:
        if json_data['operating_system']:
            l.append("\n\n## System Requirements")
            l.append("\n\nSpec     | Min. Requirement", )
            l.append("\n:----    | :----------------")
            l.append("\n**OS**   | " + json_data['operating_system'])
            l.append("\n**CPU**  | " + json_data['processor'])
            l.append("\n**HDD**  | " + json_data['hdd'])
            l.append("\n**RAM**  | " + json_data['ram'])
            l.append("\n**GPU**  | " + json_data['gpu'])
    except:
        pass

    # Media files
    l.append("\n\n## Docs\n")

    if os.path.exists(manual_path):
        l.append("\n- [Manual](manual.pdf)")

    if os.path.exists(os.path.join(user_file_dir, 'boxart.jpg')):
        l.append("\n- [Boxart](boxart.jpg)")

    if os.path.exists(os.path.join(user_file_dir, 'grid.jpg')):
        l.append("\n- [Grid](grid.jpg)")

    if os.path.exists(os.path.join(user_file_dir, 'hero.jpg')):
        l.append("\n- [Hero](hero.jpg)")

    if os.path.exists(os.path.join(user_file_dir, 'icon.png')):
        l.append("\n- [Icon](icon.png)")

    if os.path.exists(os.path.join(user_file_dir, 'screenshot.jpg')):
        l.append("\n- [Screenshot](screenshot.jpg)")

    if os.path.exists(extras_path):
        l.append("\n\n## Extras")

        for f in sorted(os.listdir(extras_path)):
            l.append("\n- [" + f.split('.')[0].title() + "](../extras/" + f + ")")

    # Write data to file
    readme = open(readme_path, 'w')
    readme.writelines(l)
    readme.close()


def create_tarfile(filename):
    clean_pfx(filename)
    with tarfile.open(filename + '.tar.gz', "w:gz") as tar:
        print('Creating tarball...')
        tar.add(filename, arcname=os.path.basename(filename))


def info_template():
    print('{\n\
  "name": "",\n\
  "title": "",\n\
  "alt_title": "",\n\
  "description": "",\n\
  "developer": "",\n\
  "publisher": "",\n\
  "esrb": "",\n\
  "genre": "",\n\
  "tags": [""],\n\
  "players": 1,\n\
  "region": "",\n\
  "system": "",\n\
  "year": 1999,\n\
  "co_op": false,\n\
  "collection": "",\n\
  "controller_support": false,\n\
  "engine": "",\n\
  "notes": "",\n\
  "online_multiplayer": false,\n\
  "save_path": "",\n\
  "store": "",\n\
  "translation": false,\n\
  "operating_system": "",\n\
  "gpu": "",\n\
  "hdd": "",\n\
  "processor": "",\n\
  "ram": ""\n}')


# WINE PFX FUNCTIONS

def clean_pfx(filename):
    pfx = get_pfx(filename)

    # Ask user to remove dotnet files
    dotnet_check = input('Would you like to remove .NET files? (y/n): ')
    if dotnet_check.lower() == 'y':
        print('Removing .NET files')
        remove_dotnet(filename)
    else:
        print('Keeping .NET files')

    # Remove all dosdevices except c:
    dosdevices = os.path.join(pfx, 'dosdevices')
    for file in os.listdir(dosdevices):
        if file != 'c:':
            os.remove(os.path.join(dosdevices, file))


def get_pfx(filename):
    if os.path.isdir(os.path.join(filename, 'drive_c')):
        pfx = filename
    elif os.path.isdir(os.path.join(filename, 'data/drive_c')):
        pfx = os.path.join(filename, 'data')
    else:
        print('Could not find prefix.')
        exit()
    return pfx


def remove_dotnet(filename):
    pfx = get_pfx(filename)
    win = os.path.join(pfx, 'drive_c/windows')

    # Dotnet file array
    dotnet_files = [
        os.path.join(win, 'Installer'),
        os.path.join(win,'Microsoft.NET'),
        os.path.join(win, 'mono'),
        os.path.join(win, 'system32/gecko'),
        os.path.join(win, 'syswow64/)gecko')]

    # Remove dotnet files if present
    for d in dotnet_files:
        if os.path.isdir(d):
            shutil.rmtree(d)


# DB FUNCTIONS

def sqlite_query(query):
    try:
        CURSOR.execute(query)
    except sqlite3.OperationalError as e:
        print('There was a problem with the SQLite query: ', e)


'''Get sorted list of tags from DB'''


def sort_tags():
    tag_list = []
    tags_json = os.path.join(Config.JSON, 'tags.json')

    if not os.path.exists(Config.JSON):
        os.makedirs(Config.JSON)

    try:
        tag_query = CURSOR.execute('select tags from game where 1;')
    except sqlite3.OperationalError as e:
        print(e)
        exit()

    '''Split comma-seperated tags and add to array.'''
    for t in tag_query:
        if t[0]:
            tag_string = t[0].split(', ')
            for ts in tag_string:
                tag_list.append(ts)

    '''Create unique list and filter redundancies'''
    unique_list = []

    for x in tag_list:
        if x not in unique_list:
            unique_list.append(x)

    sorted_tags = sorted(unique_list)

    '''Dump data to file'''
    with open(tags_json, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(sorted_tags, indent=4))


def export_games():
    games_export = os.path.join(Config.JSON, 'library/games.json')
    subprocess.run(['sqlite3', Config.DB, '.mode json', '.once ' + games_export, 'select * from game;'])


def convert_to_json(table_name):
    # export_dir = os.path.join(Config.PROFILE_DIR, 'export')
    export_path = os.path.join(EXPORT_DIR, table_name + '.json')

    if not os.path.isdir('export'):
        os.makedirs('export')

    CURSOR.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in CURSOR.description]
    results = []

    for row in CURSOR.fetchall():
        result = dict(zip(columns, row))
        results.append(result)

    with open(export_path, 'w') as f:
        json.dump(results, f, indent=4)

    message = "export complete"
    return message


def import_table(table):
    game_json = os.path.join(EXPORT_DIR, table + '.json')
    game_data = json.load(open(game_json))

    for row in game_data:
        columns = ', '.join(row.keys())
        placeholders = ', '.join('?' * len(row))
        sql = 'INSERT INTO {} ({}) VALUES ({})'\
            .format(table, columns, placeholders)
        print(sql)
        CURSOR.execute(sql, tuple(row.values()))

    CONNECTION.commit()

import_table(os.path.join(EXPORT_DIR, 'genres.json'))

def import_all():
    # export_dir = os.path.join(Config.PROFILE_DIR, 'export')
    for f in os.listdir(EXPORT_DIR):
        f_name = f.split('.')[0]
        print('importing...', f_name)
        import_table(f_name)
