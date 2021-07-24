#!/usr/bin/env bash
# This script installs all of the system-level deps
# #########################
# Run as:
# $ scripts/install.sh
# #########################
# See blog post here: https://lemariva.com/blog/2020/03/tutorial-getting-started-micropython-v20
source scripts/env.sh
# Install rust toolchain (required for esptool.py dependencies)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.profile
# sudo apt-get install -y git wget flex bison gperf python3 python3-pip python3-venv python3-setuptools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0
sudo apt-get install -y wget libncurses-dev flex bison gperf python3 python3-pip python3-setuptools python3-serial python3-click python3-cryptography python3-future python3-pyparsing python3-pyelftools cmake ninja-build ccache libffi-dev libssl-dev python-is-python3
# Download the ESP-IDF framework
mkdir ~/esp/
cd ~/esp/
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
git checkout 4c81978a3e2220674a432a588292a4c860eef27b
git submodule update --init --recursive
## NOTE: the above hash is defined by the variable ESPIDF_SUPHASH_V4 in the file:
# https://github.com/micropython/micropython/blob/master/ports/esp32/Makefile

# Download the ESP-IDF toolchain. This is for the v8.2.0 r2 release compatible with esp-idf v4.0
cd ~/esp/
wget https://dl.espressif.com/dl/xtensa-esp32-elf-gcc8_2_0-esp-2019r2-linux-amd64.tar.gz
tar -xzf xtensa-esp32-elf-gcc8_2_0-esp-2019r2-linux-amd64.tar.gz

# Add the crosscompiler to our path
export PATH="$HOME/esp/xtensa-esp32-elf/bin:$PATH"
export IDF_PATH="$HOME/esp/esp-idf"   # old micropython versions
export ESPIDF="$HOME/esp/esp-idf"     # new micropython versions
# Change to the project directory, set up venv & install esp tools
cd $PROJECT_PATH
python3 -m venv venv
source venv/bin/activate

pip install esptool
