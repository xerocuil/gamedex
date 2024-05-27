import json
import os
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from lib.config import Config

# Init DB
db = SQLAlchemy()

local_device_json = os.path.join(Config.PROFILE_DIR, 'json/devices/local.json')
local_device_data = json.load(open(local_device_json))
games_path = local_device_data[0]['games_path']
local_platforms = pd.DataFrame(local_device_data[0]['platforms'])


class Utils:
    def get_filepath(platform_slug, filename):
        platform_path = local_platforms\
            .loc[local_platforms['slug'] == platform_slug]['path'].values[0]
        file_path = os.path.join(games_path, platform_path, filename)
        return file_path
