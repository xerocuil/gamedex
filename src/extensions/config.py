import os
import random
import string

from configparser import ConfigParser

# GLOBALS
EXT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(EXT_DIR)
HOME_DIR = os.path.expanduser('~')
PROFILE_DIR = os.path.join(HOME_DIR, '.gamedex')
CONFIG_PATH = os.path.join(PROFILE_DIR, 'config.ini')

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

    # Write to config.ini
    with open(CONFIG_PATH, 'w') as conf_data:
        cfg.write(conf_data)


# Create configuration files if missing
if not os.path.exists(CONFIG_PATH):
    init_config()

# Load configuration from `config.ini` file
cfg.read(CONFIG_PATH)
