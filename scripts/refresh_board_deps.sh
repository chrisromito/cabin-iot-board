#!/usr/bin/env bash
# This Medium article illustrates the process/purpose here
#     https://medium.com/@chrismisztur/pycom-uasyncio-installation-94931fc71283
cd $PROJECT_DIR
rm -rf .deps
mkdir .deps
cd ./.deps
# Get the generic micropython lib
git clone https://github.com/micropython/micropython-lib.git micropython-lib

# Extract upip so we can use it on the device itself
echo "Moving to src/lib"
mv micropython-lib/upip/upip.py ../src/lib/upip.py
mv micropython-lib/upip/upip_utarfile.py ../src/lib/upip_utarfile.py

# Get the Ublox GPS Module so we can parse NMEA sentences
#git clone https://github.com/lemariva/wipy2.0-GPS.git gps-parser
#echo "Moving Ublox GPS module..."
#mv gps-parser/ublox_gps.py ../src/lib/ublox_gps.py

cd ..
echo "Done"
