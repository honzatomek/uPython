#!/bin/bash

esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0 esp8266-512k-20191220-v1.12.bin
