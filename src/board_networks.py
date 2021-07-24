from mqtt import MQTTClient
from network import WLAN
from constants import BROKER_HOST, BROKER_PORT, WLAN_HOST, WLAN_PASSWORD


wlan = WLAN(mode=WLAN.STA)

wlan.connect(WLAN_HOST, auth=(WLAN.WPA2, WLAN_PASSWORD))


class Mqtt:
    """
    NOTE: Subclass this to implement an MQTT Broker w/ your own callback
    Your class must implement the 'callback' method, which is passed directly into
    MQTTClient().set_callback(self.callback)
    See: `setup` method
    """
    def __init__(self, device_id, host=BROKER_HOST, port=BROKER_PORT):
        self.client = MQTTClient(device_id, host, port=port)
        self.is_connected = False

    def setup(self):
        if not wlan.isconnected():
            return None
        client = self.client
        client.set_callback(self.callback)
        if not self.is_connected:
            client.connect()
            self.is_connected = True
        return client

    def subscribe(self, *args, **kwargs):
        return self.client.subscribe(**kwargs)

    def publish(self, *args, **kwargs):
        return self.client.publish(**kwargs)


