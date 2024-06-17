import json
import os
import requests
import pandas as pd

from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from lib.extensions import Config
from models.library import *

# GLOBALS
device_bp = Blueprint('device', __name__)


# FUNCTIONS

def load_devices():
    device_dir = os.path.join(Config.PROFILE_DIR, 'json', 'devices')
    device_index = []

    try:
        # Look for all .json files in the `devices` directory
        device_index += [each.split('.')[0] for each in os.listdir(device_dir) if each.endswith('.json')]
    except Exception as e:
        # Return none if no devices found.
        device_index = None
        print(e)
    return device_index


# ROUTES
@device_bp.route('/devices')
def devices():
    return render_template('/device/index.html', devices=load_devices())


@device_bp.route('/device/detail/<string:device_slug>')
def detail(device_slug):
    # Get data from device api
    device_api = request.host_url + url_for('api.device', device_slug=device_slug)
    device = requests.get(device_api).json()[0]
    games_path = device['games_path']
    for p in device['platforms']:
        p['directory'] = os.path.join(games_path, p['path'])
        if os.path.isdir(p['directory']):
            p['supported'] = True
        else:
            p['supported'] = False
    return render_template('device/detail.html', device=device)


@device_bp.route('/<string:device_slug>/platform/<string:platform_slug>')
def platform(device_slug, platform_slug):
    '''Display platform data for given device

    Args:
        device_slug (string): Device slug ID
        platform_slug (string): Platform slug ID
    '''
    # Get platform by slug
    p = db.one_or_404(db.select(Platform).filter_by(slug=platform_slug))

    # Load device data
    device_api = request.host_url + url_for('api.device', device_slug=device_slug)
    device = requests.get(device_api).json()[0]

    # Load platform data
    games_path = device['games_path']
    platform_path = os.path.join(games_path, platform_slug)
    print(platform_path)

    # List available games on HOST
    platform_json = os.path.join(Config.PROFILE_DIR, 'json')
    platform_json = os.path.join(platform_json, 'platforms')
    platform_json = os.path.join(platform_json, platform_slug + '.json')

    try:
        platform_json_data = json.load(open(platform_json))
    except FileNotFoundError as e:
        flash('Please update platform information on host.')
        print(e)
        return redirect(url_for('device.detail', device_slug=device_slug))

    platform_games = pd.DataFrame(platform_json_data['games'])

    # Query Game model
    games_db = pd.DataFrame(Game.query.with_entities(Game.id, Game.filename, Game.title, Game.platform_id))
    device_games = []
    files = []

    # Look for all games in device platform directory
    try:
        for f in os.listdir(str(platform_path)):
            if os.path.isfile(os.path.join(str(platform_path), f)):
                files.append(f)
        file_list = sorted(files)
    except FileNotFoundError as e:
        file_list = None
        flash('Platform not found.')
        print(e)

    for f in file_list:
        try:
            f = games_db.loc[games_db['filename'] == f]['filename'].values[0]
            device_games.append({
                "id": games_db.loc[games_db['filename'] == f]['id'].values[0],
                "filename": f,
                "title": games_db.loc[games_db['filename'] == f]['title'].values[0],
                "platform_id": games_db.loc[games_db['filename'] == f]['platform_id'].values[0]
            })
        except IndexError as e:
            print('Could not find ' + f)
            print(e)
            device_games.append({"filename": f})

    # Get list of available games on HOST
    available_games = []
    for filename in platform_games['filename']:
        if filename not in file_list:
            row = platform_games.loc[platform_games['filename'] == filename]
            row_dict = {"id": row['id'].values[0],
                        "filename": row['filename'].values[0],
                        "title": row['title'].values[0]}
            available_games.append(row_dict)

    return render_template('device/platform.html',
                           available_games=available_games,
                           device=device,
                           device_games=device_games,
                           platform=p)


def allowed_file(filename):  # Deprecate
    config_ext = {'json'}  # Deprecate
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in config_ext


@device_bp.route('/device/upload/config', methods=['GET', 'POST'])
def upload_config():
    import_dir = os.path.join(Config.PROFILE_DIR, 'import')
    if not os.path.isdir(import_dir):
        os.mkdir(import_dir)

    if request.method == 'POST':
        # Check if the post request contains file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(import_dir, filename))
            flash(import_dir, filename)
            return redirect(url_for('device.devices', name=filename))
        else:
            flash('File extension not permitted.')
    if request.method == 'GET':
        filename = request.args.get('name')
        print(filename)
    return render_template('/device/upload.html')
