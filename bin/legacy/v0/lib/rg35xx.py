#!/usr/bin/env python

import json
import os
import requests
import sqlite3
import subprocess
import sys
import shutil
import zipfile

import pandas as pd

from lib.config import Config
import lib.archive as archive

## Wand imports
# from wand.color import Color
# from wand.image import Image, COMPOSITE_OPERATORS
# from wand.display import display
# from wand.drawing import Drawing

try:
    CONNECTION = sqlite3.connect(Config.DB)
    CURSOR = CONNECTION.cursor()
except sqlite3.OperationalError as e:
    print('Could not find database.')
    exit()

device_json = json.load(open(os.path.join(Config.JSON, 'devices/rg35xx.json')))
device_name = device_json[0]['name']
device_path = device_json[0]['device_path']
games_path = os.path.join(device_path, device_json[0]['games_path'])
device_platforms = pd.DataFrame(device_json[0]['platforms'])


# RG35XX

'''Create display art'''
def display_img(platform, filename):
    file_slug = filename.split('.')[0]
    platform_path = os.path.join(Config.PROFILE_DIR, 'media/games/'+platform)
    boxart_path = os.path.join(platform_path, 'boxart/'+file_slug+'.jpg')
    if not os.path.exists(boxart_path):
        print('Boxart not available')
        exit()
    device_image_dir = os.path.join(platform_path, 'rg35xx')
    if not os.path.isdir(device_image_dir):
        os.makedirs(device_image_dir)
    device_image_path = os.path.join(device_image_dir, file_slug+'.png')
    base_img = Image(width=640, height=480)
    boxart = Image(filename=boxart_path)
    base_img.save(filename=device_image_path)
    bg = base_img.clone()
    bx = boxart.clone()
    bx.transform(resize='268x360')
    v_offset = ((bg.height - bx.height)/2)

    with Drawing() as draw:
        draw.composite(operator='over', left=32, top=v_offset, width=bx.width, height=bx.height, image=bx)
        draw(bg)
        bg.save(filename=device_image_path)
