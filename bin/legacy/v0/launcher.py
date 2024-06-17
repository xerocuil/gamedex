#!/usr/bin/env python

import os
import subprocess
import sys

# GLOBALS

system = sys.argv[1]
filename = sys.argv[2]
file_base = filename
file_ext = file_base.split('.')[1]
# print('file_ext', file_ext)
cores = os.path.join(os.path.expanduser('~'), '.config/retroarch/cores')


# FUNCTIONS

def start_app(game):
    print(game)
    start_file = os.path.join(game, 'start.sh')
    if os.path.exists(start_file):
        subprocess.run([start_file])


# Launch rom in RetroArch with configured core
def start_retroarch(core, game):
    core_path = os.path.join(cores, core + '.so')
    subprocess.run(['retroarch', '-L', core_path, game])


def main():
    if system == '32x':
        start_retroarch('picodrive_libretro', filename)

    if system == '3do':
        start_retroarch('opera_libretro', filename)

    if system == '3ds':
        start_retroarch('citra_libretro', filename)

    if system == 'amiga':
        start_retroarch('puae_libretro', filename)
        # os.chdir(filename)
        # subprocess.run(['fs-uae', 'conf.fs-uae', '--fullscreen'])

    if system == 'atari2600':
        start_retroarch('stella_libretro', filename)

    if system == 'c64':
        start_retroarch('vice_x64_libretro', filename)

    if system == 'dos':
        if os.path.isdir(filename):
            os.chdir(filename)
            subprocess.run(['dosbox', 'dosbox.bat', '-exit'])
        else:
            start_retroarch('dosbox_pure_libretro', filename)

    if system == 'dreamcast':
        start_retroarch('flycast_libretro', filename)

    if system == 'flash':
        subprocess.run(['ruffle', filename])

    if system == 'gamecube':
        subprocess.run(['dolphin-emu', '-b', '-e', filename])

    if system == 'gb':
        start_retroarch('sameboy_libretro', filename)

    if system == 'gba':
        start_retroarch('vbam_libretro', filename)

    if system == 'gbc':
        start_retroarch('sameboy_libretro', filename)

    if system == 'genesis':
        start_retroarch('picodrive_libretro', filename)

    if system == 'gg':
        start_retroarch('picodrive_libretro', filename)

    if system == 'gzdoom':
        os.chdir(os.path.dirname(filename))
        subprocess.run(['gzdoom', '-savedir', 'save', '-file', filename])

    if system == 'jaguar':
        start_retroarch('virtualjaguar_libretro', filename)

    if system == 'linux':
        start_app(filename)

    if system == 'lynx':
        start_retroarch('mednafen_lynx_libretro', filename)

    if system == 'mame':
        start_retroarch('mame_libretro', filename)

    if system == 'msx':
        start_retroarch('bluemsx_libretro', filename)

    if system == 'n64':
        # start_retroarch('parallel_n64_libretro', filename)
        if file_ext == 'z64':
            start_retroarch('parallel_n64_libretro', filename)
        if file_ext == 'n64':
            start_retroarch('mupen64plus_next_libretro', filename)

    if system == 'n64-alt':
        start_retroarch('mupen64plus_next_libretro', filename)

    if system == 'nds':
        start_retroarch('desmume_libretro', filename)

    if system == 'neo-geo':
        start_retroarch('fbneo_libretro', filename)

    if system == 'nes':
        start_retroarch('nestopia_libretro', filename)

    if system == 'ngp':
        start_retroarch('race_libretro', filename)

    if system == 'ps2':
        subprocess.run(['pcsx2-qt', '-nogui', '-fullscreen', filename])

    if system == 'ps3':
        subprocess.run(['rpcs3', '--no-gui', '--fullscreen', filename])

    if system == 'psx':
        start_retroarch('swanstation_libretro', filename)

    if system == 'psp':
        start_retroarch('ppsspp_libretro', filename)

    if system == 'saturn':
        start_retroarch('mednafen_saturn_libretro', filename)

    if system == 'scd':
        start_retroarch('picodrive_libretro', filename)

    if system == 'scummvm':
        subprocess.run(['scummvm', '-f', filename])

    if system == 'sms':
        start_retroarch('picodrive_libretro', filename)

    if system == 'snes':
        start_retroarch('snes9x_libretro', filename)

    if system == 'steam':
        subprocess.run(['steam', '-silent', '-applaunch', filename])

    if system == 'tg16':
        start_retroarch('mednafen_pce_libretro', filename)

    if system == 'vb':
        start_retroarch('mednafen_vb_libretro', filename)

    if system == 'wii':
        subprocess.run(['dolphin-emu', '-b', '-e', filename])

    if system == 'wiiu':
        subprocess.run(['cemu', filename])

    if system == 'ws':
        start_retroarch('mednafen_wswan_libretro', filename)

    if system == 'windows':
        start_app(filename)

    if system == 'xbox':
        subprocess.run(['xemu', '-full-screen', '-dvd_path', filename])


if __name__ == '__main__':
    main()
