import os
import sqlite3
import subprocess
import extensions.config as config
import gamedex.settings as settings
from library.models import Game, Platform, Tag


# GLOBALS
APP_CFG = config.cfg['APP']
APP_DIR = config.APP_DIR


# LIBRARY FUNCTIONS

def count_tags():
    """Count instance of each tag and sort descending by count.

    Returns:
        dict: List of tag dictionaries
    """

    # Open database connection
    try:
        db_conn = sqlite3.connect(APP_CFG['db'])
        db_cursor = db_conn.cursor()
    except sqlite3.OperationalError as e:
        print('Could not find database.', e)
        exit()

    # Query tags, init count list
    tags = Tag.objects.all()
    tag_count = []

    # Look up each tag and count each instance in the `library_game_tags` table
    #
    # I'm sure there is a much more elegant way to access ManytoMany fields
    # but for now I'm using the hacky SQLite way.
    for t in tags:
        db_cursor.execute(f'SELECT count(*) FROM library_game_tags WHERE tag_id == {t.id};')
        count = db_cursor.fetchone()[0]
        tag_count.append({'id': t.id, 'name': t.name, 'count': count})

    tag_count = sorted(tag_count, key=lambda x: x['count'], reverse=True)

    # Close database connection
    db_conn.close()

    return tag_count


def count_platforms():
    platform_count = []
    platforms = Platform.objects.all()
    games = Game.objects.all()

    for p in platforms:
        platform_count.append({'id': p.id, 'name': p.name, 'count': 0})

    for g in games:
        platform = next(item for item in platform_count if item['id'] == g.platform.id)
        platform['count'] = platform['count'] + 1

    platform_count = sorted(platform_count, key=lambda x: x['count'], reverse=True)

    return platform_count


def total_playtime():
    """Get total sum of play time.

    Returns:
        decimal: Sum of `play_time` column of all rows in `library_game` table.
    """
    games = Game.objects.all()
    total = 0
    for g in games:
        if g.play_time:
            if g.play_time > 0:
                total = total + g.play_time

    return total


# SYSTEM FUNCTIONS

def check_for_dir(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def check_installation():
    """Set up application database and profile directories."""

    if not os.path.exists(APP_CFG['db']):
        print('Initializing configuration...')

        # Create application directories
        profile_dir = settings.PROFILE_DIR
        check_for_dir(profile_dir)

        media_dir = os.path.join(profile_dir, 'media')
        check_for_dir(media_dir)

        sys_dir = os.path.join(profile_dir, 'sys')
        check_for_dir(sys_dir)

        db_dir = os.path.join(sys_dir, 'db')
        check_for_dir(db_dir)

        # Migrate database/collect static files
        migrate_db('library')
        collect_static()


# DJANGO FUNCTIONS

def collect_static():
    curr_dir = os.getcwd()
    os.chdir(APP_DIR)
    subprocess.run(['python', 'manage.py', 'collectstatic',  '--noinput'])
    os.chdir(curr_dir)


def migrate_db(app):
    curr_dir = os.getcwd()
    os.chdir(APP_DIR)
    subprocess.run(['python3', 'manage.py', 'makemigrations', app])
    subprocess.run(['python3', 'manage.py', 'migrate'])
    os.chdir(curr_dir)
