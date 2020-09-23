#
#   Python class for MS5611 barometric pressure sensor.
#   Samuel Dewan - 2020
#

import smbus
import struct
from enum import IntEnum
from time import sleep

class MS5611():
    ADDRESS = 0b1110110

    OSR_POS = 1
    PROM_ADDR_POS = 1

    def __init__(self, bus, csb=0):
        self.bus = bus
        self.address = MS5611.ADDRESS | csb
        self.prom = MS5611PROMData(self)

    def _fetch_prom_value(self, addr):
        command = MS5611Command.PROM_READ | addr
        val = self.bus.read_i2c_block_data(self.address, command, 2)
        return struct.unpack(">H", bytes(val))[0]

    def _do_conversion(self, command, osr):
        # Start conversion
        self.bus.write_i2c_block_data(self.address, command | osr, [])
        # Wait for conversion to complete
        sleep(0.01) 
        # Read back result
        val = self.bus.read_i2c_block_data(self.address, MS5611Command.ADC_READ,
                                           3)
        return struct.unpack(">I", bytes([0] + val))[0]

    def _get_d1(self, osr=None):
        if osr is None:
            osr = MS5611OSRSetting.OSR_4096
        return self._do_conversion(MS5611Command.D1, osr)

    def _get_d2(self, osr=None):
        if osr is None:
            osr = MS5611OSRSetting.OSR_4096
        return self._do_conversion(MS5611Command.D2, osr)

    def poll(self):
        # Get data from sensor
        d1 = self._get_d1()
        d2 = self._get_d2()
        # Calculate temperature
        dT = d2 - (self.prom[MS5611PROMAddress.C5] * 256)
        temp = int(2000 + ((dT * self.prom[MS5611PROMAddress.C6]) / 8388608))
        # Second order temperature compensation
        t2 = 0
        off2 = 0
        sens2 = 0
        if temp > 2000:
            t2 = (dT * dT) / 2147483648;
            a = (temp - 2000) * (temp - 2000)
            off2 = 5 * (a / 2)
            sens2 = 5 * (a / 4)
            if temp < -1500:
                a = (temp- 1500) * (temp - 1500)
                off2 += 7 * a
                sens2 += 11 * (a / 2)
        temp = int(temp - t2)
        # Calculate temperature compensated presure
        offset = ((self.prom[MS5611PROMAddress.C2] * 65536) +
                  ((self.prom[MS5611PROMAddress.C4] * dT) / 128)) - off2
        sensitivity = ((self.prom[MS5611PROMAddress.C1] * 32768) +
                  ((self.prom[MS5611PROMAddress.C3] * dT) / 256)) - sens2
        pressure = int((((d1 * sensitivity) / 2097152) - offset) / 32768)

        # Return pressure in mbar and temperature in celsius
        return ((pressure / 100), (temp / 100))

    def get_altitude(self, pressure=None, temp=None, p0=1013.25):
        data = None
        if pressure is None or temp is None:
            data = self.poll()
        if pressure is None:
            pressure = data[0]
        if temp is None:
            temp = data[1]

        return ((((p0 / pressure) ** 0.1902225604) - 1.0) * temp) / 0.0065

class MS5611Command(IntEnum):
    RESET = 0x1E
    D1 = 0x40
    D2 = 0x50
    ADC_READ = 0x00
    PROM_READ = 0xA0

class MS5611OSRSetting(IntEnum):
    OSR_256 = 0b000 << MS5611.OSR_POS
    OSR_512 = 0b001 << MS5611.OSR_POS
    OSR_1024 = 0b010 << MS5611.OSR_POS
    OSR_2048 = 0b011 << MS5611.OSR_POS
    OSR_4096 = 0b100 << MS5611.OSR_POS

class MS5611PROMAddress(IntEnum):
    MAN = 0 << MS5611.PROM_ADDR_POS
    C1 = 1 << MS5611.PROM_ADDR_POS
    C2 = 2 << MS5611.PROM_ADDR_POS
    C3 = 3 << MS5611.PROM_ADDR_POS
    C4 = 4 << MS5611.PROM_ADDR_POS
    C5 = 5 << MS5611.PROM_ADDR_POS
    C6 = 6 << MS5611.PROM_ADDR_POS
    CRC = 7 << MS5611.PROM_ADDR_POS

class MS5611PROMData:
    def __init__(self, sensor):
        self.cache = dict()
        self.sensor = sensor

    def __getitem__(self, key):
        if not isinstance(key, MS5611PROMAddress):
            raise KeyError(key)
        val = self.cache.get(key)
        if val is  None:
            # Value was not cached, need to get it from the sensor
            val = self.sensor._fetch_prom_value(key)
            self.cache[key] = val
        return val

