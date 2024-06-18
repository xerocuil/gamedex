import json
import os
import sqlite3
from decimal import Decimal
from django.utils import timezone

import extensions.app_context  # noqa: F401
import extensions.config as config
from library.models import Game


# GLOBALS

JSON_DIR = os.path.join(config.JSON_DIR, 'lutris')
JSON_FILE = os.path.join(JSON_DIR, 'installed.json')


# DB CONNECTION

LUTRIS_DB = os.path.join(os.path.expanduser('~'), '.local', 'share', 'lutris', 'pga.db')
LT_CONN = None
CONN_ERR = 'Could not connect to Lutris database.'

if os.path.exists(LUTRIS_DB):
    try:
        LT_CONN = sqlite3.connect(LUTRIS_DB)
        LT_CURSOR = LT_CONN.cursor()
    except sqlite3.OperationalError as e:
        print(CONN_ERR, e)
        exit()


# FUNCTIONS

def import_data():
    """Import data from Lutris Sqlite DB"""

    # Export Lutris data to JSON file and load JSON data
    export_data()

    with open(JSON_FILE, 'r') as f:
        lt_games = json.load(f)

    # Update last_played, play_time columns in `library_games`
    for g in lt_games:
        try:
            g_obj = Game.objects.values('last_played', 'play_time', 'date_modified').get(filename=g['filename'])
        except Game.DoesNotExist:
            g_obj = None

        if g_obj:
            if g['last_played']:
                if not g_obj['last_played'] or g['last_played'] > g_obj['last_played']:
                    g_obj['last_played'] = g['last_played']
                    g_obj['date_modified'] = timezone.now()
                    g_obj.save()
                    print(g_obj.slug(), 'updated last_played\n')

            if g['play_time']:
                if not g_obj['play_time'] or \
                        round(g['play_time'], 2) > round(g_obj['play_time'], 2) + Decimal(0.01):
                    g_obj['play_time'] = round(g['play_time'], 2)
                    g_obj['date_modified'] = timezone.now()
                    g_obj.save()
                    print(g_obj.slug(), 'updated play_time\n')

    print('Lutris import complete.\n')


def export_data():
    """Export Lutris data to JSON files"""

    installed_games = []
    lt_query = 'SELECT\
        slug, name, platform, lastplayed, playtime, service \
        FROM games WHERE installed = 1;'
    LT_CURSOR.execute(lt_query)
    columns = ['filename', 'title', 'platform', 'last_played', 'play_time', 'store']

    for row in LT_CURSOR.fetchall():
        game_dict = dict(zip(columns, row))
        installed_games.append(game_dict)

    for g in installed_games:
        try:
            query = Game.objects.values('id', 'title').get(filename=g['filename'])
            g['gdid'] = query['id']
            g['title'] = query['title']
        except Game.DoesNotExist:
            g['gdid'] = None

    if not os.path.isdir(JSON_DIR):
        os.makedirs(JSON_DIR)

    with open(JSON_FILE, 'w') as f:
        json.dump(installed_games, f)

    print('Lutris export complete.\n')
