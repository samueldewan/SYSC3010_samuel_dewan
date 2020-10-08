#! /usr/bin/env python3

import requests
import sys

WRITE_URL = "https://api.thingspeak.com/update.json"

# Get API key from file
try:
    with open("api_write_key.txt", "r") as keyfile:
        write_key = keyfile.read().strip()
except FileNotFoundError as e:
    print("Could not open key file.", file=sys.stderr)
    exit(1)

# Send POST request
search_params = {
    "field1" : "L3-T-2",
    "field2" : "samueldewan@cmail.carleton.ca",
    "field3" : "a",
    "key" : write_key
}

r = requests.post(WRITE_URL, params=search_params)

# Print a message based on whether the request was successful
if r.ok:
    print("Successfully wrote to channel!")
    print(r.json())
else:
    print("Failed to write to channel.", file=sys.stderr)
    exit(1)

