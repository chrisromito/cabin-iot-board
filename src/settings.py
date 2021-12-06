from micropython import const

from constants import ZERO, ONE


class Settings:
    WLAN_HOST = 'sudo'
    WLAN_PASSWORD = 'HowNowBrownCow'
    MQTT_BROKER_HOST = '192.168.0.188'
    MQTT_BROKER_PORT = '1883'
    API_URL = 'http://192.168.0.188:5000/api'
    BOARD_ID = 1

DEBUG = True
# Network
WLAN_HOST = Settings.WLAN_HOST
WLAN_PASSWORD = Settings.WLAN_PASSWORD
MQTT_BROKER_HOST = Settings.MQTT_BROKER_HOST
MQTT_BROKER_PORT = Settings.MQTT_BROKER_PORT
# LoRa config
LORA_BOARD_ID = Settings.BOARD_ID
LORA_REPEATER = 0  # Set this to 1 if this device is a repeater
# Systems & other apps
API_URL = Settings.API_URL

# Ticks == 60 per sec == 60 per 1000ms
TICK_RATE_MS = 1000 // 60
TICK_RATE_SEC = 1 / 60

# Sleep = 3 seconds
SLEEP_DURATION_MS = const(3000)

# Pins
# ############
SDA = const(23)
SCL = const(22)
TX = const(17)
RX = const(16)
VEHICLE_LED = const(14)
LOW_POWER_LED = const(32)
STATUS_LED = const(15)
BUTTON_PIN = None
# UART_BAUDRATE = const(38400)
UART_BAUDRATE = const(115200)
PROXY_TRIGGER_PIN = None
PROXY_ECHO_PIN = None

# Adapter configs
BUTTON_PIN_ADAPTER = ZERO
BUTTON_QWIIC_ADAPTER = ONE
BUTTON_ADAPTER = BUTTON_QWIIC_ADAPTER

PROXY_PIN_ADAPTER = ZERO
PROXY_QWIIC_ADAPTER = ONE
PROXY_ADAPTER = PROXY_QWIIC_ADAPTER

# Proxy thresholds, etc
PROXY_DISTANCE_THRESHOLD_CM = const(400)

# Cooling Config + mechanism thresholds (aka fan)
THERMOMETER_PIN = const(34)
FAN_PIN = const(21)
FAN_MIN_THRESHOLD_CELSIUS = const(35)
HEATING_MAX_THRESHOLD_CELSIUS = const(1)
