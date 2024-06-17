#!/usr/bin/env python

import json
import os
import shutil
import sqlite3
import sys
import tarfile
import zipfile

from ftplib import FTP
# from icecream import ic  # Debug
from io import StringIO  # Python3 use: from io import StringIO
from lib.extensions import Config

ftp = FTP(Config.FTP_HOST)

try:
    CONNECTION = sqlite3.connect(Config.DB)
    CURSOR = CONNECTION.cursor()
except sqlite3.OperationalError as e:
    print('Could not find database.', e)
    exit()


# DB FUNCTIONS
def sqlite_query(query):
    try:
        CURSOR.execute(query)
    except sqlite3.OperationalError as e:
        print('There was a problem with the SQLite query: ', e)


# FTP FUNCTIONS
def create_zipfile(platform, filename):
    cache_dir = os.path.join(Config.PROFILE_DIR, 'cache/psx')
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    file_base = os.path.basename(filename)
    file_dir = os.path.dirname(filename)
    file_slug = file_base.split('.')[0]
    host_path = os.path.join(Config.FTP_PATH, platform, file_slug + '.zip')
    # host_path = os.path.join(host_dir, file_slug + '.zip')
    repository = os.path.join('/mnt/games', platform)
    repository_path = os.path.join(repository, file_slug + '.zip')

    # Check if archive already exists
    query = ftp_query(host_path)
    if query:
        print('Archive is already in repository.')
        exit()

    # Create destination directory if it does not exist
    archive_path = os.path.join(cache_dir, file_slug + '.zip')
    archive_dest_dir = os.path.join('/mnt/games', platform)
    if not os.path.isdir(archive_dest_dir):
        os.makedirs(archive_dest_dir)

    # Create zip archive
    os.chdir(file_dir)

    try:
        with zipfile.ZipFile(archive_path, mode='x') as archive:
            print('Creating archive...')
            archive.write(file_base)
            print('Archive complete.')
    except FileExistsError as err:
        print('FILE ALREADY ARCHIVED:', err)

    print('Uploading ' + file_slug + '.zip...')
    try:
        shutil.move(archive_path, repository_path)
        shutil.rmtree(cache_dir)
        print('Upload complete.\n\n')
    except Exception as err:
        print(err, 'Error uploading archive.\n\n')


def ftp_transfer(src, dest):
    ftp = FTP(Config.FTP_HOST)
    ftp.login()

    with open(dest, 'wb') as f:
        try:
            ftp.retrbinary('RETR ' + src, f.write)
            success = True
        except Exception as e:
            print('Could not transfer file.')
            print(e)
            success = False
    ftp.quit()
    return success


def ftp_query(file):
    ftp.login()
    query = ftp.retrlines('LIST ' + file)
    query_count = query.split('\n')[1].split(' ')[1]
    ftp.quit()
    return int(query_count)


def ftp_close():
    ftp = FTP(Config.FTP_HOST)
    ftp.close()


def get_archives(platform):
    host_root = '/Games'
    host_platform = os.path.join(host_root, platform)
    ftp.login()
    std_stdout = sys.stdout
    sys.stdout = file_list = StringIO()
    query = ftp.retrlines('LIST ' + host_platform)
    sys.stdout = std_stdout
    ftp.quit()
    archives = []
    for f in file_list.getvalue().split('\n'):
        if f.endswith('.tgz'):
            archives.append(f.split(' ')[-1])
    return archives


def update_archive(platform_slug):
    platform_json = os.path.join(Config.JSON, 'platforms/' + platform_slug + '.json')

    # Get platform data from DB
    platform_query = "SELECT id, name FROM platform where slug = '" + platform_slug + "';"
    sqlite_query(platform_query)
    platform_data = CURSOR.fetchone()
    if not platform_data:
        print('Could not load platform data.')
        exit()
    platform_obj = {"id": platform_data[0], "name": platform_data[1]}

    # Query game data by platform id
    games_query = "SELECT id, filename, title FROM game where platform_id = '" + str(
        platform_data[0]) + "' ORDER BY filename;"
    sqlite_query(games_query)
    games_data = CURSOR.fetchall()

    # Get list of archive files on FTP host
    archives = get_archives(platform_slug)

    # Create game data object & make list of games not in archive
    games_obj = []
    not_in_archive = []

    for game in games_data:
        game_id = game[0]
        filename = game[1]
        title = game[2]
        game_slug = filename.split('.')[0]
        game_archive_file = game_slug + '.tgz'
        if game_archive_file in archives:
            games_obj.append({"id": game_id, "filename": filename, "title": title, "archive": game_archive_file})
        else:
            not_in_archive.append(game_archive_file)

    # Return `not in archive` list
    if len(not_in_archive) > 0:
        print('Games missing from archive:')
        print(not_in_archive)

    # Dump game object to file
    platform_obj.update({"games": games_obj})
    with open(platform_json, 'w', encoding='utf-8') as f:
        json.dump(platform_obj, f, indent=4)

    print(not_in_archive)


def create_tarball(platform_slug, filename):
    cache_dir = os.path.join(Config.PROFILE_DIR, 'cache/' + platform_slug)
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    file_base = os.path.basename(filename)
    file_dir = os.path.dirname(filename)
    file_slug = file_base.split('.')[0]
    archive_name = file_slug + '.tgz'
    host_path = os.path.join(Config.FTP_PATH, platform_slug, archive_name)
    # host_path = os.path.join(host_dir, archive_name)
    repository_dir = os.path.join('/mnt/games', platform_slug)
    repository_path = os.path.join(repository_dir, archive_name)

    '''Check if archive already exists'''
    if ftp_query(host_path):
        print('Archive is already in repository.')
        exit()

    '''Create destination directory if it does not exist'''
    archive_path = os.path.join(str(cache_dir), archive_name)
    archive_dest_dir = os.path.join('/mnt/games', platform_slug)
    if not os.path.isdir(archive_dest_dir):
        os.makedirs(archive_dest_dir)

    '''Create zip archive'''
    os.chdir(file_dir)

    with tarfile.open(archive_path, 'x') as archive:
        archive.add(file_base)
        archive.list()

    print('Uploading ' + archive_name + '...')
    try:
        shutil.move(archive_path, repository_path)
        shutil.rmtree(cache_dir)
        print('Upload complete.\n\n')
    except:
        print('Error uploading archive.\n\n')
