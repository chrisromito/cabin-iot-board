try:
    import ujson as json
except:
    import json
try:
    from utime import time
except:
    from time import time
from settings import LORA_BOARD_ID, LORA_REPEATER



class Header:
    def __init__(self, source_board_id=LORA_BOARD_ID, repeater=0, timestamp=None):
        self.source_board_id = source_board_id  # type: int
        self.repeater = repeater  # type: int
        self.timestamp = timestamp or int(time())  # type: int

    def __str__(self):
        return self.to_lora()

    def to_lora(self):
        return ','.join(
            list(
                map(str, [self.source_board_id, self.repeater, self.timestamp])
            )
        )

    @staticmethod
    def lift_str(value: str):
        source_board_id, repeater, timestamp = value.split(',')
        return Header(int(source_board_id), int(repeater), int(timestamp))

    @staticmethod
    def this_device():
        return Header(LORA_BOARD_ID, LORA_REPEATER)


class Payload:
    """
    LoRa packet data serializer/deserializer
    """

    def __init__(self, data, header: Header):
        self.data = data  # type: Union[list[float], str]
        self.header = header  # type: Header

    def data_to_lora(self) -> str:
        return json.dumps(self.data)

    def data_to_python(self) -> list[float]:
        data = self.data
        if isinstance(data, str):
            return json.loads(data)
        return data

    @staticmethod
    def of(data: list[float], header):
        return Payload(data, header)

    def to_lora(self) -> str:
        return ','.join(
            [
                self.header.to_lora(),
                self.data_to_lora(),
            ]
        ).replace(' ', '')


def payload_to_lora(payload: Payload) -> str:
    return payload.to_lora()


def lora_to_payload(lora_response: str) -> Payload:
    board_id, repeater, ts, data = lora_response.split(',', 3)
    return Payload(
        json.loads(data),
        Header(int(board_id), int(repeater), int(ts))
    )


class Packet:
    def __init__(self, data, address=0, rssi=0, snr=0):
        self.data = data  # type: str
        self.address = address  # type: int
        self.rssi = rssi  # type: int
        self.snr = snr  # type: int

    def __str__(self):
        return self.data

    @staticmethod
    def uart_to_packet(resp: str) -> Packet:
        """
        TypeError: can't convert 'str' object to bytes implicitly
        :param resp:
        :return:

        Example (decoded) UART response:  +RCV=0,9,123,1,578,-50,42\r\n
        """
        payload = resp[5:-2]  # '+RCV=0,9,123,1,578,-50,42\r\n' => '0,9,123,1,578,-50,42'
        # '0,9,123,1,578,-50,42' => ['0', '9', '123,1,578,-50,42']
        address, length, rest = payload.split(',', 2)
        # '123,1,578,-50,42' => ['123,1,578', '-50', '42']
        data, rssi, snr = rest.rsplit(',', 2)
        return Packet(data, int(address), int(rssi), int(snr))

    def to_payload(self)-> Payload:
        return lora_to_payload(self.data)

