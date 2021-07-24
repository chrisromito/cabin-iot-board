"""
Adapted from Adafruit's Raspberry Pi interface

Source: https://github.com/adafruit/Adafruit-VC0706-Serial-Camera-Library/blob/master/raspi_camera.py
"""
from micropython import const
from machine import UART
from constants import ZERO, ONE
from typing import List, Optional, Union, Any
from .shared import Buses


FIVE = const(5)
INC = const(8192)
BAUD = const(38400)
# this is the port on the Raspberry Pi; it will be different for serial ports on other systems.
PORT = "/dev/ttyAMA0"

TIMEOUT = 0.5  # I needed a longer timeout than ladyada's 0.2 value
SERIAL_NUM = ZERO  # start with 0, each camera should have a unique ID.

SEND = const(0x56)
REPLY = const(0x76)
END = ZERO

RESET = const(0x26)
TAKE_PHOTO = const(0x36)
READ_BUFF = const(0x32)
GET_BUFF_LEN = const(0x34)

FBUF_CURRENT_FRAME = ZERO
FBUF_NEXT_FRAME = ONE

FBUF_STOP_CURRENT_FRAME = ZERO

reset_command = [SEND, SERIAL_NUM, RESET, END]
take_photo_command = [SEND, SERIAL_NUM, TAKE_PHOTO, ONE, FBUF_STOP_CURRENT_FRAME]
get_buffer_len_command = [SEND, SERIAL_NUM, GET_BUFF_LEN, ONE, FBUF_CURRENT_FRAME]
read_photo_command = [SEND, SERIAL_NUM, READ_BUFF, 0x0c, FBUF_CURRENT_FRAME, 0x0a]


class Camera:
    def __init__(self, buses: Buses):
        self.serial = buses.uart
        self.is_ready = False

    async def setup(self):
        self.is_ready = True
        return True

    def take_photo(self):
        self.write(take_photo_command)
        reply: List[int] = list(self.read(5))
        return check_reply(reply, TAKE_PHOTO) and reply[3] == chr(0x0)

    def read_photo_from_buffer(self):
        return self.read_buffer(
            self.get_buffer_length()
        )

    def read_buffer(self, buffer_length: int) -> Optional[List[int]]:
        addr = 0  # the initial offset into the frame buffer
        photo: list[Any] = []
        # bytes to read each time (must be a multiple of 4)
        inc = INC
        while addr < buffer_length:
            # on the last read, we may need to read fewer bytes.
            chunk = min(buffer_length - addr, inc)
            # append 4 bytes that specify the offset into the frame buffer
            offset = [(addr >> 24) & 0xff,
                      (addr >> 16) & 0xff,
                      (addr >> 8) & 0xff,
                      addr & 0xff]
            data_to_read = [(chunk >> 24) & 0xff,
                            (chunk >> 16) & 0xff,
                            (chunk >> 8) & 0xff,
                            chunk & 0xff]
            # Piece it all together & write back
            self.write(
                read_photo_command + offset + data_to_read + [ONE, ZERO]
            )
            # the reply is a 5-byte header, followed by the image data
            #   followed by the 5-byte header again.
            reply = list(self.read(FIVE + chunk + FIVE))
            if len(reply) != FIVE + chunk + FIVE:
                # retry the read if we didn't get enough bytes back.
                continue
            if not check_reply(reply, READ_BUFF):
                print('ERROR READING PHOTO =(')
                return None
            # append the data between the header data to photo
            photo += reply[FIVE:chunk + FIVE]
            # advance the offset into the frame buffer
            addr += chunk
        return photo

    def reset(self)-> bool:
        try:
            self.write(reset_command)
            return check_reply(
                list(self.read(100)),
                RESET
            )
        except:
            print('Camera reset failed silently')
            return False

    def get_buffer_length(self) -> int:
        self.write(get_buffer_len_command)
        reply: List[int] = list(self.read(9))
        if check_reply(reply, GET_BUFF_LEN) and reply[4] == chr(0x4):
            target_bytes = (reply[6], reply[7], reply[8])
            buffer_len = reply[5]
            for target_byte in target_bytes:
                buffer_len <<= 8
                buffer_len += target_byte
            return buffer_len
        return 0

    def write(self, command: List[int]) -> Optional[int]:
        return self.serial.write(
            bytearray(command)
        )

    def read(self, n_bytes=5) -> Optional[bytes]:
        return self.serial.read(n_bytes)


def check_reply(reply: List[int], byte_num: int) -> bool:
    return (
            REPLY == reply[0]
            and SERIAL_NUM == reply[1]
            and byte_num == reply[2]
            and 0x00 == reply[3]
    )


# def reset():
#     cmd = ''.join(map(chr, reset_command))
#     s.write(cmd)
#     reply = s.read(100)
#     r = list(reply)
#     if checkreply(r, RESET):
#         return True
#     return False
#
# def takephoto():
#     cmd = ''.join(map(chr, take_photo_command))
#     s.write(cmd)
#     reply = s.read(5)
#     r = list(reply)
#     if (checkreply(r, TAKE_PHOTO) and r[3] == chr(0x0)):
#         return True
#     return False
#
# def getbufferlength():
#     cmd = ''.join(map(chr, get_buffer_len_command))
#     s.write(cmd)
#     reply = s.read(9)
#     r = list(reply)
#     if (checkreply(r, GET_BUFF_LEN) and r[4] == chr(0x4)):
#         l = ord(r[5])
#         l <<= 8
#         l += ord(r[6])
#         l <<= 8
#         l += ord(r[7])
#         l <<= 8
#         l += ord(r[8])
#         return l
#     return 0
#
# def read_buffer(buffer_bytes):
#     addr = 0  # the initial offset into the frame buffer
#     photo = []
#     # bytes to read each time (must be a multiple of 4)
#     inc = 8192
#     while addr < buffer_bytes:
#         # on the last read, we may need to read fewer bytes.
#         chunk = min(buffer_bytes - addr, inc)
#         # append 4 bytes that specify the offset into the frame buffer
#         command = read_photo_command + [(addr >> 24) & 0xff,
#                                         (addr >> 16) & 0xff,
#                                         (addr >> 8) & 0xff,
#                                         addr & 0xff]
#
#         # append 4 bytes that specify the data length to read
#         command += [(chunk >> 24) & 0xff,
#                     (chunk >> 16) & 0xff,
#                     (chunk >> 8) & 0xff,
#                     chunk & 0xff]
#
#         # append the delay
#         command += [1, 0]
#         # make a string out of the command bytes.
#         cmd = ''.join(map(chr, command))
#         s.write(cmd)
#
#         # the reply is a 5-byte header, followed by the image data
#         #   followed by the 5-byte header again.
#         reply = s.read(5 + chunk + 5)
#
#         # convert the tuple reply into a list
#         r = list(reply)
#         if len(r) != 5 + chunk + 5:
#             # retry the read if we didn't get enough bytes back.
#             continue
#         if not checkreply(r, READ_BUFF):
#             return
#         # append the data between the header data to photo
#         photo += r[5:chunk + 5]
#         # advance the offset into the frame buffer
#         addr += chunk
#     return photo

"""
Adafruit's license:
============================
 This is a library for the Adafruit TTL JPEG Camera (VC0706 chipset)

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/397

  These displays use Serial to communicate, 2 pins are required to interface

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
==========================================
"""
