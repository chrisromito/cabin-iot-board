"""
    Source: https://micronote.tech/2020/07/I2C-Bus-with-a-NodeMCU-and-MicroPython/
    Source for Complementary Filter: http://blog.bitify.co.uk/2013/11/using-complementary-filter-to-combine.html

    NOTE: The offsets toward the bottom of this file (see AccelOffset & GyroOffset)
    were obtained by taping the IMU to a table across the room from any movement (to minimize vibration),
    logging the data for several hours, then averaging all of the measurements.

    Once the aforementioned offsets were obtained, I ran all of the logged data through "get_body_frame",
    with all K values from 0.99999 - 0.50000 to see which one yields the lowest deviation from 0 values 
    ONLY ALONG THE X AND Y AXES

"""
from machine import I2C
from micropython import const
from conversions import degrees_to_rad, gravity_to_mss
from utils import map_right


# Registers & Addresses
MPU6050_ADDR = const(0x68)

MPU6050_ACCEL_XOUT_H = const(0x3B)
MPU6050_ACCEL_XOUT_L = const(0x3C)
MPU6050_ACCEL_YOUT_H = const(0x3D)
MPU6050_ACCEL_YOUT_L = const(0x3E)
MPU6050_ACCEL_ZOUT_H = const(0x3F)
MPU6050_ACCEL_ZOUT_L = const(0x40)
MPU6050_TEMP_OUT_H = const(0x41)
MPU6050_TEMP_OUT_L = const(0x42)
MPU6050_GYRO_XOUT_H = const(0x43)
MPU6050_GYRO_XOUT_L = const(0x44)
MPU6050_GYRO_YOUT_H = const(0x45)
MPU6050_GYRO_YOUT_L = const(0x46)
MPU6050_GYRO_ZOUT_H = const(0x47)
MPU6050_GYRO_ZOUT_L = const(0x48)
MPU6050_PWR_MGMT_1 = const(0x6B)

MPU6050_LSBC = 340.0
MPU6050_TEMP_OFFSET = 36.53
MPU6050_LSBG = 16384.0
MPU6050_LSBDS = 131.0

# Other constants
ONE_EIGHTY = const(180)


class Imu:
    """
    Public IMU Interface
    """
    def __init__(self, i2c):
        self.i2c = i2c
        self.is_ready = False

    async def setup(self):
        try:
            init_imu(self.i2c)
            self.is_ready = True
        except:
            self.is_ready = False
        return self.is_ready

    def next(self):
        return get_imu_data(self.i2c)

    async def async_next(self):
        return self.next()


def init_imu(i2c):
    i2c.writeto_mem(MPU6050_ADDR, MPU6050_PWR_MGMT_1, bytes([0]))


def get_imu_data(i2c):
    return {
        'temp': get_temp(i2c),
        'accel': get_accel(i2c),
        'gyro': get_gyro(i2c)
    }


map_g_to_mss = map_right(gravity_to_mss)


def get_accel(i2c):
    """
    :param I2C i2c: Bus for the IMU
    :returns float[]: x, y, z in g's
    """
    combine = read_combine(i2c, MPU6050_ADDR, MPU6050_LSBG)
    # Accelerometer returns everything in g-force
    gravity_list = [
        combine(MPU6050_ACCEL_XOUT_H, MPU6050_ACCEL_XOUT_L),
        combine(MPU6050_ACCEL_YOUT_H, MPU6050_ACCEL_YOUT_L),
        combine(MPU6050_ACCEL_ZOUT_H, MPU6050_ACCEL_ZOUT_L)
    ]
    # We want m/s^2, because... who uses g-force?
    return map_g_to_mss(gravity_list)


map_radians = map_right(degrees_to_rad)


def get_gyro(i2c):
    combine = read_combine(i2c, MPU6050_ADDR, MPU6050_LSBDS)
    rotation_list = [
        combine(MPU6050_GYRO_XOUT_H, MPU6050_GYRO_XOUT_L),
        combine(MPU6050_GYRO_YOUT_H, MPU6050_GYRO_YOUT_L),
        combine(MPU6050_GYRO_ZOUT_H, MPU6050_GYRO_ZOUT_L)
    ]
    return map_radians(rotation_list)


def get_temp(i2c):
    """
    TODO: CR 2021-Feb-24 - Do we care about temperature?

    :param I2C i2c: Bus for the IMU
    :returns int: Temperature in celcius
    """
    temp_h = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_TEMP_OUT_H, 1)
    temp_l = i2c.readfrom_mem(MPU6050_ADDR, MPU6050_TEMP_OUT_L, 1)
    return (combine_register_values(temp_h, temp_l) / MPU6050_LSBC) + MPU6050_TEMP_OFFSET


def read_combine(i2c, address, denominator):
    def combine(h, l):
        upper = i2c.readfrom_mem(address, h, 1)
        lower = i2c.readfrom_mem(address, l, 1)
        return combine_register_values(upper, lower) / denominator
    return combine


def combine_register_values(h, l):
    h_one = h[0]
    l_one = l[0]
    if not h_one & 0x80:
        return h_one << 8 | l_one
    return -((h_one ^ 255) << 8) |  (l_one ^ 255) + 1


