import network
from utime import sleep_ms

class WiFi:
    def __init__(self, ssid, password):
        self.__ssid = ssid
        self.__password = password
        self.__ap_if = network.WLAN(network.AP_IF)
        self.__sta_if = network.WLAN(network.STA_IF)

    def connect(self, timeout_ms=5000):
        self.__ap_if.active(False)
        self.__sta_if.active(True)
        print('[+] Connecting to network "{0}'.format(self.__ssid))
        self.__sta_if.connect(self.__ssid, self.__password)
        i = timeout_ms
        delay = 100
        while not self.__sta_if.isconnected():
            sleep_ms(delay)
            i -= delay
            if i <= 0:
                break
        return self.__sta_if.ifconfig()[0] != '0.0.0.0'

    def disconnect(self):
        self.__sta_if.disconnect()

    def isconnected(self):
        return self.__sta_if.isconnected()

