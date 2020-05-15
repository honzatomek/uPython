#!/bin/bash

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 sonoff-basic-r2-1M.bin
