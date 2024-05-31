#!/usr/bin/env python

import os
import subprocess
import extensions.config as config
import extensions.utils as utils

APP_CFG = config.cfg['APP']


def main():
    utils.check_installation()

    if APP_CFG['public_mode'] == 'True':
        host = '0.0.0.0'
    else:
        host = APP_CFG['server_name']

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([
        'python3',
        'manage.py',
        'runserver',
        host + ':' + APP_CFG['port']])


if __name__ == '__main__':
    main()
