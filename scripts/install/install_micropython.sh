#!/usr/bin/env bash
# #########################
# Run as:
# $ scripts/install_micropython.sh
# #########################
source scripts/env.sh
# Set up Micropython
echo '' && echo ''
echo 'Setting up local micropython installation...'
git clone --recursive https://github.com/chrisromito/micropython.git
cd micropython/mpy-cross
make

cd $PROJECT_DIR
