import json
import os

from flask import Blueprint
from lib.extensions import Config
from models.library import *

api_bp = Blueprint('api', __name__)


# API
@api_bp.route('/api/tags')
def tags():
    '''Searches all tags in database

    Returns:
        sorted_tags (list): Sorted list of all tags in database
    '''
    tags_all = [g.tags for g in Game.query.all()]
    tag_list = []
    tags_unique = []

    for ta in tags_all:
        if ta:
            tag_string = ta.split(', ')
            for ts in tag_string:
                tag_list.append(ts)

    for tl in tag_list:
        if tl not in tags_unique:
            tags_unique.append(tl)

    sorted_tags = sorted(tags_unique)
    return sorted_tags


@api_bp.route('/api/device/<string:device_slug>')
def device(device_slug):
    '''Get device configuration data

    Args:
        device_slug (str): Device slug ID

    Returns:
        device_data (obj): Device configuration data in JSON format
    '''
    device_dir = os.path.join(Config.PROFILE_DIR, 'json/devices')
    device_config_path = os.path.join(device_dir, device_slug + '.json')
    device_data = json.load(open(device_config_path))
    return device_data


@api_bp.route('/api/platform/<string:platform_slug>')
def platform(platform_slug):
    platform_dir = os.path.join(Config.PROFILE_DIR, 'json/platforms')
    platform_config_path = os.path.join(platform_dir, platform_slug + '.json')
    platform_data = json.load(open(platform_config_path))
    return platform_data
