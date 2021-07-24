#!/usr/bin/env bash
export PROJECT_DIR=$(git rev-parse --show-toplevel)
#export ESP_PORT=/dev/ttyACM0
export ESP_PORT=/dev/ttyUSB0
export AMPY_PORT=$ESP_PORT
export RSHELL_PORT=$ESP_PORT
export FIRMWARE_FILENAME=esp32-20210623-v1.16.bin
export FIRMWARE_PATH=$PROJECT_DIR/firmware/$FIRMWARE_FILENAME
export SOURCE_DIR=$PROJECT_DIR/src