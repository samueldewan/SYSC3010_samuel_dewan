#! /usr/bin/env python3

import thingspeak
import os

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

# Read data from channel
data = channel.read()
print([i['field1'] for i in data])

