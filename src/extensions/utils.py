import json
import os
import sqlite3
import subprocess
import extensions.config as config
from extensions.helpers import load_json_file, sort_title
from library.models import Game, Platform, Tag


# GLOBALS

APP_CFG = config.cfg['APP']
DIR_CFG = config.cfg['DIR']
APP_DIR = config.APP_DIR


# GAME FUNCTIONS

def scan_games():
    """Scan games directory

    Returns:
        list: Table of installed games
    """

    installed_games = []
    lutris_data = load_json_file(
        os.path.join(
            config.JSON_DIR,
            'lutris',
            'installed.json'))

    # [To-Do] Make platforms available via API
    platforms = Platform.objects.values('slug').exclude(slug__in=['steam'])

    # Scan each platform directory, add file to game list
    for platform in platforms:
        rom_list = []
        try:
            platform_dir = os.listdir(os.path.join(DIR_CFG['Games'], platform['slug']))
            for filename in platform_dir:
                # If filename is in Lutris/Steam list, remove from rom list
                if platform['slug'] == 'linux' or platform['slug'] == 'windows':
                    query = next((item['gdid'] for item in lutris_data if item['filename'] == filename), None)
                    if query:
                        platform_dir.remove(filename)
                # Skip `.discs` directories
                if not filename.endswith('.discs'):
                    rom_list.append(filename)
        except FileNotFoundError:
            platform_dir = None

        # Query each file in rom list
        for r in rom_list:
            game_dict = {}
            # If query match, add db info to game dict
            try:
                query = Game.objects.values('id', 'title').get(filename=r)
                game_dict = {
                    'id': query['id'],
                    'filename': r,
                    'title': query['title'],
                    'platform': platform['slug']
                }
                installed_games.append(game_dict)
            # If query fails, generate title from filename
            except Game.DoesNotExist:
                title = r.split('.')[0].replace('-', ' ').title()
                title = title.replace('   ', ': ').\
                    replace(' An ', ' an ').\
                    replace(' And ', ' and ').\
                    replace(' Of ', ' of ').\
                    replace(' The ', ' the ')
                title = sort_title(title, 'c')
                game_dict = {
                    'id': None,
                    'filename': r,
                    'title': title,
                    'platform': platform['slug']
                }
                installed_games.append(game_dict)

    return installed_games


def get_lutris_data():
    installed_games = []
    app_file = os.path.join(config.JSON_DIR, 'lutris', 'installed.json')
    app_data = load_json_file(app_file)

    for a in app_data:
        platform_slug = a['platform']
        installed_games.append({
            'id': a['gdid'],
            'filename': a['filename'],
            'title': a['title'],
            'platform': platform_slug.lower()
            })

    return installed_games


def get_steam_data():
    installed_games = []
    app_file = os.path.join(config.JSON_DIR, 'steam', 'installed.json')
    app_data = load_json_file(app_file)

    for a in app_data:
        installed_games.append({
            'id': a['gdid'],
            'filename': a['filename'],
            'title': a['title'],
            'platform': 'steam'
            })

    return installed_games


def get_installed_games():
    registered = []
    unregistered = []

    json_dir = os.path.join(config.JSON_DIR, 'library')
    json_file = os.path.join(json_dir, 'installed.json')

    for lg in get_lutris_data():
        if not lg['id']:
            del lg['id']
            unregistered.append(lg)
        else:
            registered.append(lg)

    for sg in get_steam_data():
        if not sg['id']:
            del sg['id']
            unregistered.append(sg)
        else:
            registered.append(sg)

    for game in scan_games():
        if not game['id']:
            del game['id']
            unregistered.append(game)
        else:
            registered.append(game)

    installed_games = {'registered': registered, 'unregistered': unregistered}

    if not os.path.isdir(json_dir):
        print(json_dir)
        os.makedirs(json_dir)

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(installed_games, f, indent=4)

    print('Installed game listing complete.')


# LIBRARY FUNCTIONS

def count_tags():
    """Generate table of tags with total game instances.

    Returns:
        list: Array of tag dictionaries
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

    # Sort tags by game count, descending
    tag_count = sorted(tag_count, key=lambda x: x['count'], reverse=True)

    # Close database connection
    db_conn.close()

    return tag_count


def count_platforms():
    """Generate table of platforms with total game instances.

    Returns:
        list: Array of platform dictionaries
    """

    # Init array and query tables
    platform_count = []
    platforms = Platform.objects.all()
    games = Game.objects.all()

    # Create platform table
    for p in platforms:
        platform_count.append({'id': p.id, 'name': p.name, 'count': 0})

    # Tally game count
    for g in games:
        platform = next(item for item in platform_count if item['id'] == g.platform.id)
        platform['count'] = platform['count'] + 1

    # Sort platforms by game count, descending
    platform_count = sorted(platform_count, key=lambda x: x['count'], reverse=True)

    return platform_count


def total_playtime():
    """Get sum of play time of all games in `library_game` table.

    Returns:
        decimal: Play time sum
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

    if not os.path.exists(config.DB_PATH):
        print('Initializing configuration...')

        # Create application directories
        for path in config.GD_DIRS:
            os.makedirs(path)

        # Migrate database/collect static files
        migrate_db('library')
        collect_static()


# DJANGO FUNCTIONS

def collect_static():
    """Collect static files and copy to profile directory."""

    curr_dir = os.getcwd()
    os.chdir(APP_DIR)
    subprocess.run(['python', 'manage.py', 'collectstatic',  '--noinput'])
    os.chdir(curr_dir)


def migrate_db(app):
    """Make database migrations and migrate"""

    curr_dir = os.getcwd()
    os.chdir(APP_DIR)
    subprocess.run(['python3', 'manage.py', 'makemigrations', app])
    subprocess.run(['python3', 'manage.py', 'migrate'])
    os.chdir(curr_dir)
