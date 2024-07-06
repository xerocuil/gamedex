import os
from configparser import ConfigParser
from extensions.helpers import generate_key, generate_server_name

# GLOBALS
EXT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(EXT_DIR)
HOME_DIR = os.path.expanduser('~')

PROFILE_DIR = os.path.join(HOME_DIR, '.gamedex')
API_DIR = os.path.join(PROFILE_DIR, 'api')
ASSETS_DIR = os.path.join(PROFILE_DIR, 'assets')
MEDIA_DIR = os.path.join(PROFILE_DIR, 'media')
SYS_DIR = os.path.join(PROFILE_DIR, 'sys')
DB_DIR = os.path.join(SYS_DIR, 'db')
GD_DIRS = [MEDIA_DIR, DB_DIR, API_DIR]

CONFIG_PATH = os.path.join(PROFILE_DIR, 'config.ini')
DB_PATH = os.path.join(PROFILE_DIR, 'sys', 'db', 'gd.db')


# Initialize config object
cfg = ConfigParser()


# FUNCTIONS

def init_config():
    """Create `config.ini` in user profile directory and load default values."""

    # General appplication configuration
    cfg['APP'] = {
        'app_title': 'GameDex',
        'debug': False,
        'db': os.path.join(
            PROFILE_DIR,
            'sys',
            'db',
            'gd.db'),
        'key': generate_key(),
        'public_mode': False,
        'server_name': generate_server_name()[0],
        'port': generate_server_name()[1]
    }

    # Directory configuration
    cfg['DIR'] = {
        'games': os.path.join(HOME_DIR, 'Games'),
    }

    # Write to config.ini
    with open(CONFIG_PATH, 'w') as f:
        cfg.write(f)


# Create configuration files if missing
if not os.path.exists(CONFIG_PATH):
    init_config()

# Load configuration from `config.ini` file
cfg.read(CONFIG_PATH)
