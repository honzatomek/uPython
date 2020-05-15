#!/bin/bash

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash -fs 1MB -fm dout 0x0 ./firmware/sonoff-basic-r2-1M.bin
