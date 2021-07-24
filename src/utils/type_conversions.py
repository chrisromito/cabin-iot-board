from typing import Any, Union


ByteOrByteArray = Union[bytes, bytearray]


def bytes_to_int(value) -> int:
    try:
        return int.from_bytes(value, 'big')
    except Exception as outer_err:
        try:
            return int.from_bytes(bytearray([value]), 'big')
        except:
            raise outer_err


def is_bytes(thing: Any) -> bool:
    return isinstance(thing, (bytes, bytearray))
