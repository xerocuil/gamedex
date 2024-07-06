import json
import os
import sqlite3
from decimal import Decimal
from django.utils import timezone

# import extensions.app_context  # noqa: F401
import extensions.config as config
# from library.models import Game
import extensions.sqlite_man as sqlite_man

# GLOBALS

API_DIR = os.path.join(config.API_DIR, 'lutris')
JSON_FILE = os.path.join(API_DIR, 'installed.json')
DB_PATH = os.path.join(os.path.expanduser('~'), '.local', 'share', 'lutris', 'pga.db')


lutris_db = sqlite_man.SqliteDB(DB_PATH)
gamedex_db = sqlite_man.SqliteDB(config.DB_PATH)


# FUNCTIONS

def import_data():
    """Import data from Lutris Sqlite DB"""

    # Export Lutris data to JSON file and load JSON data
    export_data()

    with open(JSON_FILE, 'r') as f:
        lt_games = json.load(f)

    # Update last_played, play_time columns in `library_games`
    for g in lt_games:
        print('\nLooking for', g['title'], '...')
        try:
            query = 'SELECT title, id, last_played, play_time, date_modified FROM library_game WHERE filename == "' + g['filename'] + '";'

            result = gamedex_db.g(query)
        except Exception:
            result = None
            print(g['filename'], 'not found in database.')

        if result:
            if g['last_played']:
                if not result['last_played'] or g['last_played'] > result['last_played']:
                    result['last_played'] = g['last_played']
                    result['date_modified'] = timezone.now()
                    update_lastplayed = 'UPDATE library_game SET last_played = "' +\
                        str(result['last_played']) +\
                        '", date_modified = "' +\
                        str(result['date_modified']) +\
                        '" WHERE id = "' +\
                        str(result['id']) + '";'
                    gamedex_db.cursor.execute(update_lastplayed)

            if g['play_time']:
                if not result['play_time'] or \
                        round(g['play_time'], 5) > Decimal(round(result['play_time'], 5)) + Decimal(0.0001):
                    result['play_time'] = round(g['play_time'], 5)
                    result['date_modified'] = timezone.now()
                    update_playtime = 'UPDATE library_game SET play_time = "' +\
                        str(result['play_time']) +\
                        '", date_modified = "' +\
                        str(result['date_modified']) +\
                        '" WHERE id = "' + str(result['id']) + '";'
                    gamedex_db.cursor.execute(update_playtime)

    print('\nImport complete.\n')
    gamedex_db.conn.commit()
    gamedex_db.conn.close()


def export_data():
    """Export Lutris data to JSON files"""

    installed_games = []
    lt_query = 'SELECT\
        slug, name, platform, lastplayed, playtime, service \
        FROM games WHERE installed = 1;'
    lutris_db.cursor.execute(lt_query)
    columns = ['filename', 'title', 'platform', 'last_played', 'play_time', 'store']

    for row in lutris_db.cursor.fetchall():
        game_dict = dict(zip(columns, row))
        installed_games.append(game_dict)

    for g in installed_games:
        try:
            # query = Game.objects.values('id', 'title').get(filename=g['filename'])
            query = 'SELECT id, title, FROM games WHERE filename = ' + g['filename'] + ';'
            # query = Game.objects.values('id', 'title').get(filename=g['filename'])
            g['gdid'] = query['id']
            g['title'] = query['title']
        except Exception:
            g['gdid'] = None

    if not os.path.isdir(API_DIR):
        os.makedirs(API_DIR)

    with open(JSON_FILE, 'w') as f:
        json.dump(installed_games, f)

    print('Lutris export complete.\n')
