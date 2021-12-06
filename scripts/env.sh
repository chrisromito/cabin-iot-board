#!/usr/bin/env bash
echo "Setting up cabin-iot-board env..."
export PROJECT_DIR=$(git rev-parse --show-toplevel)
source $PROJECT_DIR/.env
echo "...env is good to go"
