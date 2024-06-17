#!/usr/bin/env python

import glob
import json
import os
import random
import subprocess
import sys
import threading
import time
import webview

import pandas as pd

from lib.config import Config
from main import Api as api
from icecream import ic

FTP_HOST = Config.FTP_HOST
FTP_PORT = Config.FTP_PORT
FTP_PATH = Config.FTP_PATH
DEVICES_DIR = os.path.join(Config.PROFILE_DIR, 'devices')

DEVICE_NAME = 'RG35XX'


'''Load Device Config'''
try:
    DEVICE_CONFIG_PATH = os.path.join(DEVICES_DIR, DEVICE_NAME+'.json')
    DEVICE_CONFIG = json.load(open(DEVICE_CONFIG_PATH))
except FileNotFoundError as e:
    print('Config file not found. Searching for imports...')
    import_config()
    # xlsx_path = os.path.join(DEVICES_DIR, DEVICE_NAME+'.xlsx')
    # if os.path.exists(xlsx_path):
    #     print(DEVICE_NAME+'.xlsx found. Importing...')
    #     xlsx_df = pd.read_excel(xlsx_path)
    #     print(xlsx_df)


DEVICE_NAME = DEVICE_CONFIG[0]['name']
DEVICE_PATH = DEVICE_CONFIG[0]['path']
DEVICE_PLATFORMS = pd.DataFrame(DEVICE_CONFIG[0]['platforms'])

# DEVICE_PATH = '/run/media/'+os.getlogin()+'/ROMS'
# CONFIGDIR = os.path.join(DEVICE, 'CFW/config')
# COREMAPPING = os.path.join(CONFIGDIR, 'coremapping.json')
# MAMECSV = os.path.join(CONFIGDIR, 'mame.csv')
# EXCLFILE = os.path.join(APPDIR, 'exclude.txt')


# LOCAL_CFW = os.path.join(APPDIR, 'CFW')
# DEVICE_CFW = os.path.join(DEVICE, 'CFW')



def check_device():
    if not os.path.isdir(DEVICE_PATH):
        print('Device is NOT mounted.')
        mnt = False
    else:
        print('Device is mounted.')
        mnt = True

    return mnt

def rsync(options, progress):
    if progress.lower() == 'true':
        print('show progress')

    rsync_cmd = ['rsync', options, '--delete-after', '--exclude-from='+EXCLFILE, LOCAL_CFW+'/', DEVICE_CFW+'/']

    if progress.lower() == 'true':
        rsync_cmd.append('--progress')
    return rsync_cmd

def update():
    if check_device():
        # Check rsync dry run stdout
        rsync_log = subprocess.Popen(rsync('-hirun', 'False'), stdout=subprocess.PIPE)

        # If dry run returns output, confirm sync with user
        if rsync_log.stdout.readline():
            subprocess.run(rsync('-hirun', 'False'))
            cont = str(input('\nContinue with sync? [y/n]: '))
            if cont.lower() == 'y':
                subprocess.run(rsync('-hru', 'True'))
        else:
            print('No files to sync.')
    else:
        print('Device not mounted.')



# def main():
#     try:
#         globals()[COMMAND]()
#     except NameError as e:
#         print('COMMAND ERROR:')
#         print(e)
#     except KeyError as e:
#         print('KEY ERROR:')
#         print(e)


# if __name__ == '__main__':
#     main()