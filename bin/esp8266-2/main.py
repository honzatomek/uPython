# <---------------------------------------------------- global imports ---> {{{1
import machine
from machine import Pin, ADC, RTC
from utime import sleep_ms
import time
import ntptime
from SHT30 import SHT30
from umqtt.robust import MQTTClient
from json import dumps

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
        print(message)
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
    machine.reset()


def measure():
    sensor = SHT30()
    sensor.set_delta(DELTA_T, DELTA_H)
    adc = ADC(ME.ADC)
    temperature = 0.0
    humidity = 0.0
    voltage = 0.0

    for i in range(10):
        t, h = sensor.measure()
        v = adc.read()
        temperature += float(t)
        humidity += float(h)
        voltage += float(v)
        sleep_ms(100)

    temperature /= 10.0
    humidity /= 10.0
    voltage /= 10.0

    tm = time.localtime(int(time.time() + 3600))

    data = dict()
    data['temperature'] = {'value': temperature, 'units': 'C'}
    data['humidity'] = {'value': humidity, 'units': '%'}
    data['voltage'] = {'value': voltage, 'units': 'V'}
    data['date'] = {'value': '{0:04}/{1:02}/{2:02}'.format(tm[0], tm[1], tm[2]), 'units': ''}
    data['time'] = {'value': '{0:02}:{1:02}:{2:02}.{3:03}'.format(tm[3], tm[4], tm[5], tm[6]), 'units': ''}

    return data

# <-------------------------------------------------------------- main ---> {{{1
try:
    # connect to wifi
    myprint('[i] Connecting to Wifi: {0:s}'.format(WLAN_SSID))
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
            else:
                LED.value(0)
                sleep_ms(100)
            break
        except WLANException as e:
            myprint('[-] Main: {0}'.format(e))
            myprint('[-] WLAN connection {0} to {1} not successful..'.format(i, WLAN_SSID))
        except Exception as e:
            myprint('[-] Unhandled Exception occured:\n{0}\n[-] Resetting!'.format(e))
            machine.reset()

    LED.value(1)

    # check if wemos was woken from deep sleep, if from reset, then allow 10 secs for REPL interrupt
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        myprint('[i] machine has been woken from deep sleep')
    else:
        for i in range(DELAY):
            myprint('[i] {0} seconds left to interrupt.'.format(DELAY - i))
            sleep_ms(1000)

    # connect to mqtt
    try:
        mqtt = MQTTClient(MQTT_UNAM, MQTT_BRKR, MQTT_PORT)
        mqtt.connect(clean_session=False)
        myprint('[+] Connected to MQTT Broker {0}:{1} as {2}'.format(MQTT_BRKR, MQTT_PORT, MQTT_UNAM))
    except Exception as e:
        myprint('[-] Connection to MQTT Broker failed:\n{0}\n    Resetting...'.format(e))
        machine.reset()

    # set correct time
    myprint('[i] Setting correct time')
    errcnt = 0
    ntptime.host = '192.168.1.5'
    ntptime.settime()
    myprint(f'[+] Current time: {str(RTC().datetime()):s}')

    # read temperature, humidity and voltage as mean values from 1s of measurement
    myprint('[i] Measuring data')
    data = measure()

    for key in ['date', 'time', 'temperature', 'humidity', 'voltage']:
        myprint('[i] {0}: {1} {2}'.format(key, data[key]['value'], data[key]['units']))

    try:
        myprint('[i] Publishing MQTT Topic {0:s}: {1:s}'.format(f'/senzor/{MQTT_TPOU:s}', dumps(data)))
        mqtt.publish(f'/senzor/{MQTT_TPOU:s}', dumps({MQTT_TPOU: data}))
        sleep_ms(1000)
    except Exception as e:
        myprint('[-] MQTT publish failed,\n{0}\n    Resetting...'.format(e))
        raise e
        # machine.reset()

except Exception as e:
    myprint(f'[-] Exception occured: {str(e):s}')
    pass

deep_sleep(DEEPSLEEP * 60 * 1000)

