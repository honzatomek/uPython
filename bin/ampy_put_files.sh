for f in *.py; do ampy --port /dev/ttyUSB0 --baud 115200 put "${f}"; done
