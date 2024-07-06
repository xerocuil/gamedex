import json
import os
import vdf

import extensions.app_context  # noqa: F401
import extensions.config as config
from library.models import Game


# GLOBALS

HOME_DIR = os.path.expanduser('~')
DEFAULT_STEAM_LIBRARY = os.path.join(HOME_DIR, '.steam', 'steam')
DEFAULT_STEAM_DIR = os.path.join(HOME_DIR, '.steam')
USER_LIBRARY = os.path.join(config.cfg['DIR']['games'], 'steam')
STEAM_APPS = os.path.join(USER_LIBRARY, 'steamapps')
REGISTRY_FILE = os.path.join(DEFAULT_STEAM_DIR, 'registry.vdf')

API_DIR = os.path.join(config.API_DIR, 'steam')
JSON_FILE = os.path.join(API_DIR, 'installed.json')


# FUNCTIONS

def export_data():
    """Export Steam data to JSON files"""
    installed_games = []

    try:
        for file in os.listdir(STEAM_APPS):
            if file.endswith('.acf'):
                file_data = vdf.load(open(os.path.join(STEAM_APPS, file)))
                installed_games.append({
                    'title': file_data['AppState']['name'],
                    'filename': file_data['AppState']['appid']
                    })

            for g in installed_games:
                try:
                    query = Game.objects.values('id', 'title').get(filename=g['filename'])
                    g['gdid'] = query['id']
                    g['title'] = query['title']
                except Game.DoesNotExist:
                    g['gdid'] = None

        if not os.path.isdir(API_DIR):
            os.makedirs(API_DIR)

        with open(JSON_FILE, 'w') as f:
            json.dump(installed_games, f)

        print('Steam export complete.\n')

    except Exception as e:
        print('Error during export task:\n', e)
