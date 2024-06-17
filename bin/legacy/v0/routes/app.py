from flask import Blueprint, send_from_directory
from lib.extensions import Config

app_bp = Blueprint('app', __name__)


@app_bp.route('/media/<path:path>')
def media(path):
    return send_from_directory(Config.MEDIA, path)


@app_bp.route('/json/<path:path>')
def json(path):
    return send_from_directory(Config.JSON, path)
