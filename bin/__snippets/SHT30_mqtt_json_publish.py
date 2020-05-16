# --------------------------------------------------------------------------- embedded modules
print('\n[i] importing embedded modules')
import machine
from utime import sleep_ms
from ujson import dumps, loads
from umqtt.simple import MQTTClient

# -------------------------------------------------------------------------- personal modules
print('[i] reading in custom modules')
from config import *
from SHT30 import SHT30
from wifi import WiFi

# -------------------------------------------------------------------------- global variables
print('[i] assigning global variables')
DELTA_T = -4.2
DELTA_H = 16.6

# ---------------------------------------------------------------------------- help functions
def blink(number=3, duration=250):
    print('[i] running function: blink({0})'.format(number))
    led = machine.Pin(2, machine.Pin.OUT, value=1)
    for i in range(2 * number):
        led.value(not led.value())
        sleep_ms(duration)

# ----------------------------------------------------------------------------- main function
print('[i] main function')
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

print('[i] setting up wifi connection')
wifi = WiFi(WIFI_SSID, WIFI_PW)
if not wifi.isconnected():
    try:
        wifi.connect()
    except Exception:
        print('[-] wifi connection timeout, entering deep sleep')
        rtc.alarm(rtc.ALARM0, PUBLISH_DELAY)
        machine.deepsleep()
print('[i] connected to {0} wifi'.format(WIFI_SSID))
blink(3)

print('[i] setting up mqtt client')
mqtt = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
mqtt.connect()

sensor = SHT30()
sensor.set_delta(DELTA_T, DELTA_H)

print('[i] running measure and publish')
data = dict()
t, h = sensor.measure()
if isinstance(t, float) and isinstance(h, float):
    data['temperature'] = {'value': t, 'units': 'C'}
    data['humidity'] = {'value': h, 'units': '%'}
    mqtt.publish(TOPIC_OUT, dumps(data))
    blink(5)
else:
    print('[-] corrupted sensor measurement')

print('[+] entering deep sleep')
rtc.alarm(rtc.ALARM0, PUBLISH_DELAY)
machine.deepsleep()
