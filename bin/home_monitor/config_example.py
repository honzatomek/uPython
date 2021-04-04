DEBUG = True                    # turn print function on/off
DELAY = 10                      # seconds allowed for interrupt after hard reset

DEEPSLEEP = 5 * 60 * 1000       # deep sleep timeout

WLAN_HOST = 'wemos'             # wlan dhcp_hostname prefix, 4 last chars of mac address will be appended
WLAN_SSID = '************'      # wireless network ssid
WLAN_PASS = '*********'         # wireless network password
WLAN_RTRY = 3                   # number of retries for wlan connection to WLAN_SSID
WLAN_DLAY = 5000                # delay in ms to wait for successful connection to WLAN_SSID in one try

MQTT_BRKR = '************'      # mqtt broker ip address
MQTT_PORT = 1883                # mqtt broker port
MQTT_UNAM = 'obyvak'            # not yet implemented
MQTT_PASS = None                # not yet implemented

MQTT_TPIN = '/in'               # inbound topic suffix - resulting topic will be dhcp_hostname + MQTT_TPIN
MQTT_TPOU = '/out'              # outbound topic suffix - resulting topic will be dhcp_hostname + MQTT_TPOU

DELTA_T = 0.0
DELTA_H = 0.0
VOLTAGE_COEFF = 2.46667
