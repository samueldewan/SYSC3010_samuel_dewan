#! /usr/bin/env python3

import requests
import sqlite3

apiKey = "a808bbf30202728efca23e099a4eecc7"

# Query the user for a city
city = input("Enter the name of a city whose weather you want: ")

# Get weather information
address = "http://api.openweathermap.org/data/2.5/weather"
r = requests.get(address, params = {"appid" : apiKey, "units" : "metric",
                                    "q" : city})
data = r.json()

# Check for error
if not r.ok:
    print(f"Error getting weather: {data['message']}.")
    exit(1)

# Print weather information
print(f"Temperature: {data['main']['temp']} °C")
print(f"Humidity: {data['main']['humidity']}%")
print(f"Pressure: {data['main']['pressure']} hPa")
print(f"Wind speed: {data['wind']['speed']} m/s")

# Open database
db = sqlite3.connect("my.db")

# Create weather table if it does not already exist
with db:
    db.execute('CREATE TABLE IF NOT EXISTS "weather" ("id" INTEGER NOT NULL '
               'UNIQUE, "city" TEXT, "temp" REAL, "humidity" INTEGER, '
               '"pressure" INTEGER, "windspeed" REAL, "timestamp" DATETIME '
               'DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY("id" AUTOINCREMENT))')

# Log weather information to database
with db:
    db.execute('INSERT INTO "weather" ("city", "temp", "humidity", "pressure", '
               '"windspeed") VALUES (?, ?, ?, ?, ?)', (city.lower(),
               data['main']['temp'], data['main']['humidity'],
               data['main']['pressure'], data['wind']['speed']))

# Close database
db.close()

