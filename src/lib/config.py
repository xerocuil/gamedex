#!/usr/bin/env python

import os
import random
import string
from configparser import ConfigParser

LIB_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(LIB_DIR)

HOME_DIR = os.path.expanduser('~')
PROFILE_DIR = os.path.join(HOME_DIR, '.gamedex')
CONFIG_PATH = os.path.join(PROFILE_DIR, 'config.ini')
MEDIA = os.path.join(PROFILE_DIR, 'media')
JSON = os.path.join(PROFILE_DIR, 'json')

# Get scraper keys
if os.getenv('FLASK_DEBUG'):
    MG_API_KEY = os.getenv('MG_API_KEY')
    GB_API_KEY = os.getenv('GB_API_KEY')
    SS_PASSWD = os.getenv('SS_PASSWD')
    SS_DEBUG = os.getenv('SS_DEBUG')
else:
    MG_API_KEY = None
    GB_API_KEY = None
    SS_PASSWD = None
    SS_DEBUG = None


def init_config():
    """Create `config.ini` in user profile directory."""

    # Create 'profiles' directory if missing
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
        os.makedirs(MEDIA)
        os.makedirs(JSON)

    # Create config.ini
    conf['APP'] = {
        'app_id': str(os.getenv('APP_ID')),
        'app_title': str(os.getenv('APP_TITLE')),
        'debug': os.getenv('FLASK_DEBUG'),
        'db': os.path.join(PROFILE_DIR, 'db.sqlite3'),
        'media': MEDIA,
        'json': JSON,
        'key': generate_key()
        # 'server_name': 'http://127.0.0.10:8080' Deprecated
    }

    conf['GAMES'] = {
        'games_dir': os.path.join(HOME_DIR, 'Games'),
        'roms_dir': os.path.join(HOME_DIR, 'Games/roms')  # Deprecate
    }

    conf['RETROARCH'] = {
        'exec': os.path.join(HOME_DIR, '.local', 'bin', 'retroarch'),
        'cores': os.path.join(HOME_DIR, '.config/retroarch/cores')
    }

    conf['ES'] = {
        'exec': '/usr/bin/emulationstation',
        'profile': os.path.join(HOME_DIR, '.emulationstation')
    }

    conf['FTP'] = {
        'host': '192.168.0.100',
        'port': 21,
        'path': 'Games'
    }

    # conf['SCRAPERS'] = {
    #     'mg_api_key': None,
    #     'gb_api_key': None,
    #     'ss_passwd': None,
    #     'ss_debug': None
    # }

    # Write to config.ini
    with open(CONFIG_PATH, 'w') as conf_data:
        conf.write(conf_data)


def generate_key():
    '''Generate Flask key

    Returns:
        key (str): Randomly generated 64 character key
    '''
    key = ''.join(
        random.SystemRandom()
            .choice(string.ascii_letters + string.digits) for _ in range(64))
    return key


conf = ConfigParser()
conf.read(CONFIG_PATH)

if not os.path.exists(CONFIG_PATH):
    init_config()


class Config:
    """
    ## Config

    Application configuration class.

    Attributes:
        APP_ID (str): Application slug ID
        APP_TITLE (str): Application title
        CONFIG_PATH (str): Path to configuration file
        DB (str): Database path
        DEBUG (bool): Debug mode
        KEY (str): Application key
        PROFILE_DIR (str): Path to user profile directory
        JSON (str): Path to JSON path for API
        MEDIA (str): Path to `media` directory
        GAMES_DIR (str): Path to `games` directory
        FTP_HOST (str): Host name for FTP server
        FTP_PORT (int): Port number for FTP server (default: 21)
        FTP_PATH (str): Path to games on FTP server
        GB_API_KEY (str): Giant Bomb API key
        MG_API_KEY (str): Moby Games API key
        SS_DEBUG (str): ScreenScraper debug ID
        SS_PASSWD (str): ScreenScraper password
    """

    # App settings
    APP_DIR = APP_DIR
    APP_ID = conf['APP']['app_id']
    APP_TITLE = conf['APP']['app_title']
    CONFIG_PATH = CONFIG_PATH
    DB = conf['APP']['db']
    DEBUG = int(conf['APP']['debug'])
    KEY = conf['APP']['key']
    PROFILE_DIR = PROFILE_DIR
    JSON = conf['APP']['json']  # Deprecate
    MEDIA = conf['APP']['media']  # Deprecate

    # Game settings
    GAMES_DIR = conf['GAMES']['games_dir']  # Deprecate
    ROMS_DIR = conf['GAMES']['roms_dir']  # Deprecate

    # Host settings
    FTP_HOST = conf['FTP']['host']
    FTP_PORT = conf['FTP']['port']
    FTP_PATH = conf['FTP']['path']
    GB_API_KEY = conf['SCRAPERS']['gb_api_key']
    MG_API_KEY = conf['SCRAPERS']['mg_api_key']
    SS_DEBUG = conf['SCRAPERS']['ss_debug']
    SS_PASSWD = conf['SCRAPERS']['ss_passwd']
    SHOW_MC = int(conf['SETTINGS']['show_mc'])
