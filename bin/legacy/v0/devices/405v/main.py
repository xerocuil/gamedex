#!/usr/bin/env python

import csv
import json
import os
import subprocess
import sys


import pandas as pd
from ftplib import FTP
from icecream import ic


platform = sys.argv[1]
filename = sys.argv[2]

## ANBERIC 405V
'''Install file from FTP server to 405V device'''
def install_game(platform, filename):

    game_slug = filename.split('.')[0]
    archive_name = game_slug+'.zip'
    host_file_url = '/Games/'+platform+'/'+archive_name
    ic(game_slug, archive_name, host_file_url)


    # profile_dir = os.path.dirname(Config.CONFIG_PATH)
    # cache_dir =  os.path.join(profile_dir, 'cache')
    # cache_path = os.path.join(cache_dir, archive_name)
    # platform_path = os.path.join(Config.GAMES_DIR, platform)

    # if not os.path.exists(cache_dir):
    #     os.makedirs(cache_dir)

    # if not os.path.exists(platform_path):
    #     os.makedirs(platform_path)

    # ic(archive_name, platform_path) # Debug

    # ftp = FTP(Config.FTP_HOST)
    # ftp.login()

    # with open(cache_path, 'wb') as file:
    #     try:
    #         ftp.retrbinary('RETR '+host_file_url, file.write)
    #     except:
    #         print('could not transfer')
    #         os.remove(cache_path)
    # ftp.quit()

    # subprocess.run(['7z', 'x', '-y', '-o'+platform_path, cache_path])
    # os.remove(cache_path)
    # os.rmdir(cache_dir)



if __name__ == '__main__':
    install_game(platform, filename)