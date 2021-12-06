#!/usr/bin/env bash
esptool.py --chip esp32 --port $ESP_PORT erase_flash
