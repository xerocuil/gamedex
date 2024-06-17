#!/usr/bin/env python

import glob
import json
import os
import subprocess
import sys

import pandas as pd
from icecream import ic


# GLOBALS
APPDIR = os.path.dirname(os.path.abspath(__file__))
LOCALROMS = os.path.join(os.path.expanduser( '~' ), 'Games/roms')
# REPO = '/mnt/public/Games/roms'


DEVICE = '/run/media/'+os.getlogin()+'/ROMS'
CONFIGDIR = os.path.join(DEVICE, 'CFW/config')
COREMAPPING = os.path.join(CONFIGDIR, 'coremapping.json')
MAMECSV = os.path.join(CONFIGDIR, 'mame.csv')
EXCLFILE = os.path.join(APPDIR, 'exclude.txt')


LOCAL_CFW = os.path.join(APPDIR, 'CFW')
DEVICE_CFW = os.path.join(DEVICE, 'CFW')

try:
    COMMAND = sys.argv[1]
except:
    COMMAND = None

try:
    ARGS = sys.argv[2]
except:
    ARGS = None

# SYSTEM SLUG/DEVICE DIRECTORY
SYSTEMS = {
  "2600": "ATARI",
  "32x": "MD",
  "3do": "PANASONIC",
  "amiga": "AMIGA",
  "mame": "ARCADE",
  "gb": "GBC",
  "gba": "GBA",
  "gbc": "GBC",
  "genesis": "MD",
  "gg": "GG",
  "lynx": "LYNX",
  "neo-geo": "NEOGEO",
  "nes": "FC",
  "ngp": "NGP",
  "pico": "PICO",
  "ports": "PORTS",
  "psx": "PS",
  "scd": "MD",
  "sms": "MS",
  "snes": "SFC",
  "tg16": "PCE",
  "ws": "WS"
}

def check_device():
    if not os.path.isdir(DEVICE):
        notification_stdout('Device is NOT mounted.')
        mnt = False
    else:
        notification_stdout('Device is mounted.')
        mnt = True

    return mnt

# EXTRACT FILE
# def extract_rom(system, slug):
#     check_device(DEVICE)

#     # Get directory value from slug key
#     romdir = SYSTEMS.get(system)

#     # Configure directories
#     archivedir = os.path.join(REPO, system)
#     destdir = os.path.join(LOCALROMS, romdir)
#     tarfile = os.path.join(archivedir, slug+'.tar.gz')

#     # Extract tarball
#     if os.path.exists(tarfile):
#         subprocess.run(['tar', 'xvf', tarfile, '-C', destdir])
#     else:
#         files = glob.glob(os.path.join(archivedir, slug+'.*'))
#     for file in files:
#         print(file)
#         subprocess.run(['cp', '-nrv', file, destdir])


def print_help():
    print('\n\
RG35XX Utils\n\
--------------\n\n\
Usage: main.py <COMMAND> <ARUGMENT>\n\
')

def notification_stdout(string):
    print('\n'+string+'\n')

def rsync(options, progress):
    if progress.lower() == 'true':
        notification_stdout('show progress')

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
            notification_stdout('No files to sync.')
    else:
        notification_stdout('Device not mounted.')

def debug():
    ic(os.getenv('APP_ID'))

    try:
        ic(sys.argv[1])
    except IndexError:
        notification_stdout('No COMMAND given.')

    try:
        ic(sys.argv[2])
    except IndexError:
        notification_stdout('No ARGS given.')


    if check_device():
        notification_stdout('Core map found.')
        ic(COREMAPPING)

        with open(COREMAPPING, "r") as core_data:
            cores = json.load(core_data)
            ic(cores['AMIGA'])
    else:
        print('No core file')

def main():
    try:
        globals()[COMMAND]()
    except NameError as e:
        notification_stdout('COMMAND ERROR:')
        print(e)
        debug()
    except KeyError as e:
        notification_stdout('KEY ERROR:')
        print(e)
        debug()


if __name__ == '__main__':
    main()