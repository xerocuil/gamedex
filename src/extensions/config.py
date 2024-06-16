import os
import random
import string

from configparser import ConfigParser


# GLOBALS
EXT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(EXT_DIR)
HOME_DIR = os.path.expanduser('~')
PROFILE_DIR = os.path.join(HOME_DIR, '.gamedex')
MEDIA_DIR = os.path.join(PROFILE_DIR, 'media')
SYS_DIR = os.path.join(PROFILE_DIR, 'sys')
DB_DIR = os.path.join(SYS_DIR, 'db')
ASSETS_DIR = os.path.join(PROFILE_DIR, 'assets')
JSON_DIR = os.path.join(SYS_DIR, 'assets', 'json')
CONFIG_PATH = os.path.join(PROFILE_DIR, 'config.ini')
DB_PATH = os.path.join(PROFILE_DIR, 'sys', 'db', 'gd.db')
GD_DIRS = [MEDIA_DIR, DB_DIR, JSON_DIR]


# Initialize config object
cfg = ConfigParser()


# FUNCTIONS
def generate_key():
    """Returns:
        key (str): Randomly generated 64 character key
    """
    key = ''.join(
        random.SystemRandom()
            .choice(string.ascii_letters + string.digits) for _ in range(64))
    return key


def generate_server_name():
    """Returns:
        server_name (arr): Generated IP, port
    """
    ip_sfx = random.randrange(2, 255)
    port = random.randrange(8100, 8999)
    pfx = '127.0.0.'
    ip_addr = pfx + str(ip_sfx)
    server_name = [ip_addr, port]
    return server_name


def init_config():
    """Create `config.ini` in user profile directory."""

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
