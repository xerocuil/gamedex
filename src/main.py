#!/usr/bin/env python

import os
import subprocess
import extensions.config

app_cfg = extensions.config.cfg['APP']

if app_cfg['public_mode'] == 'True':
    host = '0.0.0.0'
else:
    host = app_cfg['server_name']


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([
        'python3',
        'manage.py',
        'runserver',
        host + ':' + app_cfg['port']])


if __name__ == '__main__':
    main()
