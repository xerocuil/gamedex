#! /bin/bash

source /opt/empr/utils/utils.sh

CMD="$1"
FILE="$2"

## Run Empr
empr.run(){
  django.start
  sleep 2
  $CMS/browser/Empr-linux-x64/Empr
  django.stop
}

## Organize/Edit CMS photos in digikam
empr.gallery(){
  digikam --config $PHOTODB/photodb.ini --database-directory $PHOTODB
}

## Game launchers
3d0(){
  retroarch -L $CORES/opera_libretro.so "$FILE"
}
amiga(){
  retroarch -L $CORES/puae_libretro.so "$FILE"
}
arcade(){
  mame "$FILE" -skip_gameinfo
}
atari-2600(){
  retroarch -L $CORES/stella_libretro.so "$FILE"
}
c64(){
  retroarch -L $CORE/vice_x64_libretro.so "$FILE"
}
dreamcast(){
  retroarch -L $CORES/flycast_libretro.so "$FILE"
}
gamecube(){
  dolphin-emu -b -e "$FILE"
}
gba(){
  retroarch -L $CORES/mgba_libretro.so "$FILE"
}
gbc(){
  retroarch -L $CORES/sameboy_libretro.so "$FILE"
}
gg(){
  retroarch -L $CORES/picodrive_libretro.so "$FILE"
}
genesis(){
  retroarch -L $CORES/picodrive_libretro.so "$FILE"
}
jaguar(){
  retroarch -L $CORES/virtualjaguar_libretro.so "$FILE"
}
love(){
  love "$FILE"
}
sms(){
  retroarch -L $CORES/picodrive_libretro.so "$FILE"
}
n64(){
  retroarch -L $CORES/mupen64plus_next_libretro.so "$FILE"
}
n64-alt(){
  retroarch -L $CORES/parallel_n64_libretro.so "$FILE"
}
nes(){
  retroarch -L $CORES/nestopia_libretro.so "$FILE"
}
neo-geo(){
  BASE=${FILE%.*}
  EXT=${FILE#$BASE.}
  if [[ $EXT = "zip" ]]; then
    mame -skip_gameinfo -bios unibios40 "$FILE"
  elif [[ $EXT = "chd" ]]; then
    mame -skip_gameinfo -bios unibios40 neocdz -cdrm "$FILE"
  fi
}
ngp(){
  retroarch -L $CORES/race_libretro.so "$FILE"
}
ps1(){
  retroarch -L $CORES/mednafen_psx_libretro.so "$FILE"
}
ps2(){
  pcsx2-qt "$FILE"
}
ps2-alt(){
  pcsx2-qt --nogui --fullscreen "$FILE"
}
psp (){
  retroarch -L $CORES/ppsspp_libretro.so "$FILE"
}
saturn(){
  retroarch -L $CORES/mednafen_saturn_libretro.so "$FILE"
}
sega-cd(){
  retroarch -L $CORES/picodrive_libretro.so "$FILE"
}
snes(){
  retroarch -L $CORES/snes9x_libretro.so "$FILE"
}
turboduo(){
  retroarch -L $CORES/mednafen_pce_libretro.so "$FILE"
}
vb(){
  retroarch -L $CORES/mednafen_vb_libretro.so "$FILE"
}
wii(){
  dolphin-emu -b -e "$FILE"
}
wonderswan(){
  retroarch -L $CORES/mednafen_wswan_libretro.so "$FILE"
}
xbox(){
  xemu -full-screen -dvd_path "$FILE"
}

$CMD
