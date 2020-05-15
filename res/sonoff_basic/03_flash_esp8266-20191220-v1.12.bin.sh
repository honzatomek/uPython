#!/bin/bash

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --verify -fs 1MB -fm dout 0x0 ./firmware/esp8266-20191220-v1.12.bin

# -fs 1MB : use the flash_id command to get flash size (--flash_size=detect does not work well)
# -fm dout: needed, without it the REPL did not work
# --verify: not needed, obsolete command, now esptool verifies after each write
