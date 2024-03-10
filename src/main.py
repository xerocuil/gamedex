#!/usr/bin/env python
import json
import os

import shutil
import tarfile
import webview

import pandas as pd
from flask import Flask
from lib.extensions import db, Config
from routes.api import api_bp
from routes.app import app_bp
from routes.device import device_bp
from routes.library import library_bp
from routes.nav import nav_bp

import lib.archive as archive
import lib.rg35xx as rgw


def create_app():
    # Initialize Flask settings and register blueprints.
    new = Flask(__name__, template_folder='templates')
    new.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + Config.DB
    new.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    new.config['SECRET_KEY'] = Config.KEY
    new.config['FLASK_DEBUG'] = Config.DEBUG
    db.init_app(new)
    new.register_blueprint(api_bp)
    new.register_blueprint(app_bp)
    new.register_blueprint(device_bp)
    new.register_blueprint(library_bp)
    new.register_blueprint(nav_bp)
    return new


app = create_app()

if not os.path.exists(Config.DB):
    print("Initializing database...")
    with app.app_context():
        db.create_all()


class JsApi:
    '''
    ## JsApi

    API for bridging front-end JavaScript functions
    with back-end Python functions.
    '''

    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    # WINDOW FUNCTIONS

    def close_window(self):
        """Close application window"""
        window.destroy()

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        window.toggle_fullscreen()

    # INSTALLATION FUNCTIONS

    def install_game(self, device_slug, platform_slug, filename):
        """Install Game to device

        Example:
            install_game('local', 'dos', 'breakout.zip')

        Args:
            device_slug (str): Device slug ID
            platform_slug (str): Platform slug ID
            filename (str): Game file name

        Returns:
            game_data (:object: `dict`): Game data
        """
        file_slug = filename.split('.')[0]
        file_archive = file_slug + '.tgz'
        archive_src = os.path.join(
            Config.FTP_PATH, platform_slug, file_archive)
        cache_dir = os.path.join(Config.PROFILE_DIR, 'cache')
        archive_dest = os.path.join(cache_dir, file_archive)
        device_json_path = os.path.join(
            Config.JSON,
            'devices',
            device_slug + '.json')
        device_json = json.load(open(device_json_path))
        platform_dir = os.path.join(
            str(device_json[0]['games_path']), platform_slug)
        file_path = os.path.join(str(platform_dir), filename)

        if not os.path.exists(platform_dir):
            print('Creating platform directory...')
            os.makedirs(platform_dir)

        # Check if game is installed
        if os.path.exists(file_path):
            print('Game is already installed.')
            exit()

        # Copy file to cache directory
        if not os.path.isdir(cache_dir):
            os.makedirs(cache_dir)

        print('Transferring ' + file_archive + '...')

        if archive.ftp_transfer(archive_src, archive_dest):
            print('Transfer complete.')
        else:
            print('Could not transfer archive.')
            os.remove(archive_dest)
            exit()

        # Create platform directory if missing
        if not os.path.exists(platform_dir):
            os.makedirs(platform_dir)

        # Extract tarball to platform directory
        print('Extracting ' + file_archive + '...')
        print('archive_dest', archive_dest)

        try:
            tarball = tarfile.open(archive_dest, 'r')
            tarball.extractall(platform_dir)
            print('Extraction complete.')
        except FileNotFoundError as e:
            print(e)
            exit()

        # Clear cache
        print('Clearing cache.')
        os.remove(archive_dest)

        # Functions for Anberic RG35XX
        if device_slug == 'rg35xx':
            # Get image
            print('Fetching game image...')
            image_src = os.path.join(
                Config.PROFILE_DIR,
                'media',
                'games',
                platform_slug,
                'rg35xx',
                file_slug + '.png')
            image_dest_dir = os.path.join(str(platform_dir), 'imgs')
            image_dest = os.path.join(str(image_dest_dir), file_slug + '.png')

            if not os.path.exists(image_dest_dir):
                os.makedirs(image_dest_dir)

            if not os.path.exists(image_src):
                rgw.display_img(platform_slug, filename)

            shutil.copyfile(image_src, image_dest)

            # Update game list
            print('Updating device game list...')
            device_path = device_json[0]['path']
            csvfile = os.path.join(device_path, 'CFW', 'config', 'mame.csv')
            platform_json = os.path.join(
                Config.JSON,
                'platforms',
                platform_slug + '.json')
            platform_data = json.load(open(platform_json))
            platform_games_df = pd.DataFrame(platform_data['games'])
            csvdf = pd.read_csv(csvfile)
            if (csvdf['slug'].eq(file_slug)).any():
                print(file_slug + ' is in the gamelist.')
            else:
                title = platform_games_df
                title = title.loc[platform_games_df['filename'] == filename]
                title = title['title'].values[0]
                print('Adding ' + title + ' to gamelist...')
                csvdf.loc[len(csvdf.index)] = [file_slug, title]
                csvdf.sort_values(by=['slug']).to_csv(csvfile, index=False)

        print('Installation complete.')
        response = {"device": device_slug,
                    "platform": platform_slug,
                    "filename": filename,
                    "message": "Installed " + filename + " to " + device_slug}
        return response

    def uninstall_game(self, device_slug, platform_slug, filename):
        file_slug = filename.split('.')[0]
        device_json = json.load(open(os.path.join(
            Config.JSON,
            'devices',
            device_slug + '.json'
        )))
        games_path = os.path.join(device_json[0]['games_path'])
        device_platforms = pd.DataFrame(device_json[0]['platforms'])
        path = device_platforms.loc[device_platforms['slug'] == platform_slug]
        path = path['path'].values[0]
        platform_dir = os.path.join(str(games_path), path)
        file_path = os.path.join(platform_dir, filename)

        if os.path.exists(file_path):
            print('Removing', file_path)
            os.remove(file_path)
        else:
            print(file_path, 'not found.')
            exit()

        if device_slug == 'rg35xx':
            img_path = os.path.join(platform_dir, 'imgs/' + file_slug + '.png')

            if os.path.exists(img_path):
                print('Removing', img_path)
                os.remove(img_path)
            else:
                print(img_path + ' not found.')

        game_data = [{
            "device": device_slug,
            "platform": platform_slug,
            "filename": filename,
            "message": "Removed " + filename + " from " + device_slug
        }]

        return game_data


window = webview.create_window(
    os.getenv('APP_TITLE'),
    app, js_api=JsApi(),
    draggable=True,
    min_size=(1280, 720),
    text_select=True)


def main():
    webview.start(debug=True)

    # Debug
    # app.run()


if __name__ == '__main__':
    main()
