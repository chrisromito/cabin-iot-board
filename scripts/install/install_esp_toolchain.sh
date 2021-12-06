#!/usr/bin/env bash
# #########################
# Run as:
# $ scripts/install_esp_toolchain.sh
# #########################
source scripts/env.sh || return 1

#################################
# Install rust toolchain (required for esptool.py dependencies)
echo 'Installing rust...'
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.profile

#################################
echo '' && echo ''
echo 'Installing system prerequisites && ESP-IDF Framework. This will take like 30 minutes, sorry...'
# Prerequisites
# Docs: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/linux-setup.html
sudo apt-get install -y wget flex bison gperf python3 python3-pip python3-setuptools cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0

# ESP-IDF framework
# Docs: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html#step-2-get-esp-idf
echo '' && echo ''
mkdir ~/esp/
cd ~/esp/
git clone https://github.com/espressif/esp-idf.git
cd esp-idf
git checkout v4.3.1
git submodule update --init --recursive

# ESP-IDF toolchain
# Docs: https://docs.espressif.com/projects/esp-idf/en/v4.3.1/esp32/api-guides/tools/idf-tools.html
echo '' && echo ''
echo 'Downloading ESP-IDF toolchain'
cd ~/esp/
wget https://github.com/espressif/crosstool-NG/releases/download/esp-2021r1/xtensa-esp32-elf-gcc8_4_0-esp-2021r1-linux-amd64.tar.gz
tar -xzf xtensa-esp32-elf-gcc8_4_0-esp-2021r1-linux-amd64.tar.gz
# Add the crosscompiler to our path
export PATH="$HOME/esp/xtensa-esp32-elf/bin:$PATH"
export IDF_PATH="$HOME/esp/esp-idf"   # old micropython versions
export ESPIDF="$HOME/esp/esp-idf"     # new micropython versions

cd $PROJECT_DIR