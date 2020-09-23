#! /usr/bin/python3

#
#   This program prints the barometric pressure and temperature as determined by
#   a TE Connectivity MS5611 barometric presssure sensor connected via I2C. It
#   also calculates the current altitude above sea level.
#
#   All of the work for interfacing with the sensor and doing the related
#   calculations has been encapuslated in a seperate module, ms5611.py.
#

import smbus
import ms5611

bus = smbus.SMBus(1)


sensor = ms5611.MS5611(bus)

# Read the pressure and temperature values from the sensor
data = sensor.poll()

print(f"Pressure: {data[0]} mbar\nTemperature: {data[1]} ℃")

# Reuse data when calculating altitude so that we don't have to poll the
# sensor twice
altitude = sensor.get_altitude(pressure=data[0], temp=data[1])

print(f"Altitude: {round(altitude, 2)} m above sea level")


bus.close()

