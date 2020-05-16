from config import *
from wifi import WiFi
from machine import Pin
from utime import sleep_ms

led = Pin(2, Pin.OUT, value=1)
wifi = WiFi(WIFI_SSID, WIFI_PW)
connected = wifi.isconnected()
print('[i] WiFi {0} connected: {1}'.format(WIFI_SSID, connected))
if connected:
    print('[i] Disconnecting WiFi.')
    wifi.disconnect()


connected = wifi.connect()
print('[i] WiFi {0} connected: {1}'.format(WIFI_SSID, connected))
if connected:
    for i in range(6):
        led.value(not led.value())
        sleep_ms(250)

