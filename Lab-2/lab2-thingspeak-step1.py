#! /usr/bin/env python3

import thingspeak
import os
from time import sleep

chan_id = 1154788

# Get API keys from file
try:
    with open("api_write_key.txt", "r") as keyfile:
        write_key = keyfile.read().strip()
    with open("api_read_key.txt", "r") as keyfile:
        read_key = keyfile.read().strip()
except FileNotFoundError as e:
    print("Could not open keyfiles.")
    exit(1)

# Create channel object
channel = thingspeak.Channel(chan_id, write_key=write_key, read_key=read_key)

# Write data to channel
while True:
    # Get temperature
    temp = 0.0
    if os.path.isfile("/sys/class/thermal/thermal_zone0/temp"):
        with open("/sys/class/thermal/thermal_zone0/temp", 'r') as temp_file:
            temp = int(temp_file.read().strip()) / 1000
    # Send to thingspeak
    entry = channel.write({"Temperature": temp})
    print(entry)

    sleep(10)

