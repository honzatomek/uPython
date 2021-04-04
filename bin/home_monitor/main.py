# <---------------------------------------------------- global imports ---> {{{1
import machine
from machine import Pin, ADC, RTC
from utime import sleep_ms
import time
from SHT30 import SHT30
from umqtt.robust import MQTTClient
from json import dumps
import ntptime

# <---------------------------------------------------- custom imports ---> {{{1
from wemos import WemosD1Mini
from wlan import WLAN, WLANException

# <-------------------------------------------------- global variables ---> {{{1
from config import WLAN_SSID, WLAN_PASS, WLAN_HOST, WLAN_RTRY, WLAN_DLAY
from config import MQTT_BRKR, MQTT_PORT, MQTT_UNAM, MQTT_TPIN, MQTT_TPOU
from config import DEBUG, DELAY
from config import DELTA_T, DELTA_H, VOLTAGE_COEFF
from config import DEEPSLEEP
ME = WemosD1Mini()
LED = Pin(ME.LED, Pin.OUT, value=1)

# <----------------------------------------------------- help funcions ---> {{{1
def myprint(message=None):
    if DEBUG:
        myprint(message)
    else:
        pass

def deep_sleep(delay=300000):
    '''
    deep sleep function, default delay = 1000 * 60 * 5 = 300000 ms = 5 mins
    GPIO16 must be connected to RST (D0 to RST)
    '''
    rtc = RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    myprint('[i] Entering deep sleep for {0:.2f} min ({1} ms).'.format(delay / 60 / 1000, delay))
    rtc.alarm(rtc.ALARM0, delay)
    machine.deepsleep()

def measure():
    sensor = SHT30()
    sensor,set_delta(DELTA_T, DELTA_H)
    adc = ADC(ME.ADC)
    temperature = 0.0
    humidity = 0.0
    voltage = 0.0

    for i in range(10):
        t, h = sensor.measure()
        v = adc.read()
        temperature += float(t)
        humidity += float(h)
        voltage += ffloat(v)
        sleep_ms(100)

    temperature /= 10.0
    humidity /= 10.0
    voltage /= 10.0

    tm = RTC().datetime()

    data = dict()
    data['temperature'] = {'value': temperatrue, 'units': 'C'}
    data['humidity'] = {'value': humidity, 'units': '%'}
    data['voltage'] = {'value': voltage, 'units': 'V'}
    data['date'] = {'value': '{0:04}/{1:02}/{2:02}'.format(tm[0], tm[1], tm[2]), 'units': ''}
    data['time'] = {'value': '{0:02}:{1:02}:{2:02}.{3:03}'.format(tm[4], tm[5], tm[6], tm[7]), 'units': ''}

    return data

# <-------------------------------------------------------------- main ---> {{{1
# connect to wifi
wlan = WLAN(WLAN_SSID, WLAN_PASS)
wlan.set_hostname(WLAN_HOST)
i = 1
while i < WLAN_RTRY:
    i += 1
    try:
        if wlan.connect(delay=WLAN_DLAY):
            myprint('[+] WLAN connected to {0} as {1}.'.format(WLAN_SSID, wlan.ip()))
        if DEBUG:
            # blink 3 times to indicate wifi connected
            for i in range(3 * 2 + 1):
                LED.value(i % 2)
                sleep_ms(250)
        break
    except WLANException as e:
        myprint('[-] Main: {0}'.format(e))
        myprint('[-] WLAN connection {0} to {1} not successful..'.format(i, WLAN_SSID))
    except Exception as e:
        myprint('[-] Unhandled Exception occured:\n{0}\n[-] Resetting!'.format(e))
        machine.reset()

# check if wemos was woken from deep sleep, if from reset, then allow 10 secs for REPL interrupt
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    myprint('[i] machine has been woken from deep sleep')
else:
    for i in range(DELAY):
        print('[i] {0} seconds left to interrupt.'.format(DELAY - i))
        sleep_ms(1000)

# connect to mqtt
try:
    mqtt = MQTTClient(MQTT_UNAM, MQTT_BRKR, MQTT_PORT)
    mqtt.connect(clean_session=False)
    myprint('[+] Connected to MQTT Broker {0}:{1} as {3}'.format(MQTT_BRKR, MQTT_PORT, MQTT_UNAM))
except Exception as e:
    print('[-] Connection to MQTT Broker failed:\n{0}\n    Resetting...'.format(e))
    machine.reset()

# set correct time
ntptime.settime()  # set the rtc datetime from the remote server

# read temperatrue, humidity and voltage as mean values from 1s of measurement
data = measure()

for key in ['date', 'time', 'temperatrue', 'humidity', 'voltage']:
    myprint('[i] {0}: {1} {2}'.format(key, data[key]['value'], data[key]['units']

try:
    mqtt.publish(MQTT_TPOU, dumps(data))
except Exception as e:
    print('[-] MQTT publish failed,\n{0}\n    Resetting...'.format(e))

myprint('[i] Starting deep sleep for {0:.2f} minutes.'.format(DEEPSLEEP))
# deepsleep(DEEPSLEEP)

