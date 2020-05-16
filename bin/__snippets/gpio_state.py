# embedded modules
print('\n[i] importting embedded modules')
from machine import Pin
from utime import sleep_ms

GPIO = {0: ['GPIO0', 'D3', 'flash'],
        1: ['GPIO1', 'TX', 'UART RX'],
        2: ['GPIO2', 'D4', 'on-board led'],
        3: ['GPIO3', 'RX', 'UART TX'],
        4: ['GPIO4', 'D2', 'SDA'],
        5: ['GPIO5', 'D1', 'SCL'],
        12: ['GPIO12', 'D6', 'MISO'],
        13: ['GPIO13', 'D7', 'MOSI'],
        14: ['GPIO14', 'D5', 'SCK'],
        15: ['GPIO15', 'D8', 'SCK'],
        16: ['GPIO16', 'D0', 'wake-up pin from deep sleep']}

print('[i] {0:>6} {1:^4} {2}'.format('GPIO', 'NAME', 'Note'))
for pin in GPIO.keys():
    print('[i] {0:>6} {1:^4} {2}'.format(GPIO[pin][0], GPIO[pin][1], GPIO[pin][2]))
