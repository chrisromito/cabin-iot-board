#!/usr/bin/env bash
# Source: https://gist.github.com/tychop/29bd4af2b5492d55623b2754a2f37208
# Ampy script to mirror current directory to a microcontroller
source ./scripts/env.sh
cd $PROJECT_DIR

function rshellRsync() {
  rshell rsync --mirror $SOURCE_DIR /
}

rshellRsync
