#!/usr/bin/env bash
# This script installs all of the system-level deps
# #########################
# Run as:
# $ scripts/install/install.sh
# #########################
# See blog post here: https://lemariva.com/blog/2020/03/tutorial-getting-started-micropython-v20

#################################
# Set up environment variables
source scripts/env.sh

# ESP toolchain & micropython setup
echo 'Installing toolchains....'
source scripts/install/install_esp_toolchain.sh

# Local micropython
echo 'Installing local micropython...'
source scripts/install/install_micropython.sh

#################################
# Change to the project directory, set up venv & install esp tools
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate

pip install esptool
pip install -r requirements.txt