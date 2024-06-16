import json
import os
import sqlite3
from decimal import Decimal
from django.utils import timezone

import extensions.app_context
import extensions.config as config

from library.models import Game


# GLOBALS
JSON_DIR = os.path.join(config.JSON_DIR, 'lutris')
JSON_FILE = os.path.join(JSON_DIR, 'installed.json')
# NDB_JSON = os.path.join(JSON_DIR, 'ndb.json')


# Database connection (Lutris)
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


def import_data():
    """Import data from Lutris Sqlite DB

    Returns:
        dict: Lutris table data
    """

    # Export Lutris data to JSON file and load JSON data
    export_data()

    with open(JSON_FILE, 'r') as f:
        lt_games = json.load(f)

    # Update last_played, play_time columns in `library_games`
    for g in lt_games:
        try:
            g_obj = Game.objects.get(filename=g['slug'])
        except Game.DoesNotExist:
            g_obj = None

        if g_obj:
            if g['lastplayed']:
                if not g_obj.last_played or g['lastplayed'] > g_obj.last_played:
                    g_obj.last_played = g['lastplayed']
                    g_obj.date_modified = timezone.now()
                    g_obj.save()
                    print(g_obj.slug(), 'updated last_played\n')

            if g['playtime']:
                if not g_obj.play_time or \
                        round(g['playtime'], 2) > round(g_obj.play_time, 2) + Decimal(0.01):
                    g_obj.play_time = round(g['playtime'], 2)
                    g_obj.date_modified = timezone.now()
                    g_obj.save()
                    print(g_obj.slug(), 'updated play_time\n')

    print('Lutris import complete.\n')


def export_data():
    """Export Lutris data to JSON files"""

    installed_games = []
    lt_query = 'SELECT\
        directory, lastplayed, name, platform, playtime, service, slug\
        FROM games WHERE installed = 1;'
    LT_CURSOR.execute(lt_query)
    columns = [description[0] for description in LT_CURSOR.description]

    for row in LT_CURSOR.fetchall():
        result = dict(zip(columns, row))
        installed_games.append(result)

    for g in installed_games:
        try:
            query = Game.objects.get(filename=g['slug'])
            g['gdid'] = query.id
        except Game.DoesNotExist:
            g['gdid'] = None

    if not os.path.isdir(JSON_DIR):
        os.makedirs(JSON_DIR)

    with open(JSON_FILE, 'w') as f:
        json.dump(installed_games, f, indent=4)

    print('Lutris export complete.\n')
