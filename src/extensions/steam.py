import json
import os
import vdf

import extensions.app_context
import extensions.config as config

from library.models import Game


HOME_DIR = os.path.expanduser('~')
DEFAULT_STEAM_LIBRARY = os.path.join(HOME_DIR, '.steam', 'steam')
DEFAULT_STEAM_DIR = os.path.join(HOME_DIR, '.steam')
USER_LIBRARY = os.path.join(config.cfg['DIR']['games'], 'steam')
STEAM_APPS = os.path.join(USER_LIBRARY, 'steamapps')
REGISTRY_FILE = os.path.join(DEFAULT_STEAM_DIR, 'registry.vdf')

JSON_DIR = os.path.join(config.JSON_DIR, 'steam')
JSON_FILE = os.path.join(JSON_DIR, 'installed.json')


def export_data():
    """Export Steam data to JSON files"""
    installed_games = []

    for file in os.listdir(os.path.join(STEAM_APPS)):
        if file.endswith('.acf'):
            file_data = vdf.load(open(os.path.join(STEAM_APPS, file)))
            manifest_data = {
                'title': file_data['AppState']['name'],
                'filename': file_data['AppState']['appid']
                }
            installed_games.append(manifest_data)

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

    print('Steam export complete.\n')
