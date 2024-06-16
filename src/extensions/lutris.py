import json
import os
import sqlite3

import extensions.app_context
import gamedex.settings
from library.models import Game


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

    if not LT_CONN:
        print(CONN_ERR)
        return None

    LT_CURSOR.execute('SELECT * FROM games')
    columns = [description[0] for description in LT_CURSOR.description]
    lutris_data = []
    in_db = []
    not_in_db = []

    for row in LT_CURSOR.fetchall():
        result = dict(zip(columns, row))
        lutris_data.append(result)

    for data in lutris_data:
        lg = Game.objects.filter(filename__icontains=data['slug'])
        if lg:
            for i in lg:
                if i.filename == data['slug'] or i.slug() == data['slug']:
                    if data['lastplayed']:
                        i.last_played = data['lastplayed']
                    if data['playtime']:
                        i.play_time = data['playtime']
                    i.save()
                    in_db.append(data)
                    break
        else:
            not_in_db.append(data)

    lutris_export = os.path.join(gamedex.settings.PROFILE_DIR, 'sys', 'json', 'lutris.json')
    lutris_missing = os.path.join(gamedex.settings.PROFILE_DIR, 'sys', 'json', 'lutris_ndb.json')

    with open(lutris_export, 'w') as f:
        json.dump(in_db, f, indent=4)

    with open(lutris_missing, 'w') as f:
        json.dump(not_in_db, f, indent=4)


def export_installed_games():
    lutris_dir = os.path.join(
        os.path.expanduser('~'),
        '.gamedex', 'sys', 'json', 'lutris')
    lutris_json = os.path.join(lutris_dir, 'games.json')
    lt_query = 'SELECT\
        directory, installed, lastplayed, name, platform, playtime, service, slug\
        FROM games WHERE installed = 1;'
    LT_CURSOR.execute(lt_query)
    columns = [description[0] for description in LT_CURSOR.description]
    results = []

    for row in LT_CURSOR.fetchall():
        result = dict(zip(columns, row))
        results.append(result)

    for r in results:
        try:
            model_q = Game.objects.get(filename=r['slug'])
        except Game.DoesNotExist:
            model_q = None

        if model_q:
            r['idb'] = 1
        else:
            r['idb'] = 0

    if not os.path.isdir(lutris_dir):
        os.makedirs(lutris_dir)

    with open(lutris_json, 'w') as f:
        json.dump(results, f, indent=4)
