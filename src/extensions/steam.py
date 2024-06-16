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

JSON_DIR = os.path.join(config.PROFILE_DIR, 'sys', 'assets', 'json', 'steam')
JSON_FILE = os.path.join(JSON_DIR, 'installed.json')


def export_data():
    installed_games = []

    for file in os.listdir(os.path.join(STEAM_APPS)):
        if file.endswith('.acf'):
            file_data = vdf.load(open(os.path.join(STEAM_APPS, file)))
            manifest_data = {
                'name': file_data['AppState']['name'],
                'appid': file_data['AppState']['appid']
                }
            installed_games.append(manifest_data)

        for g in installed_games:
            try:
                query = Game.objects.get(filename=g['appid'])
                g['gdid'] = query.id
            except Game.DoesNotExist:
                g['gdid'] = None

    if not os.path.isdir(JSON_DIR):
        os.makedirs(JSON_DIR)

    with open(JSON_FILE, 'w') as f:
        json.dump(installed_games, f, indent=4)

    print('Steam export complete.\n')
