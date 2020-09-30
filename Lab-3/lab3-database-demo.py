#! /usr/bin/env python3

import sqlite3
from datetime import datetime

# Open database
db = sqlite3.connect("my.db")

# Create the temperature table if it does not already exist
with db:
    db.execute('CREATE TABLE IF NOT EXISTS "temperature" ("id" INTEGER NOT NULL '
               'UNIQUE, "tempfloat" NOT NULL, "datetext" NOT NULL, PRIMARY '
               'KEY("id" AUTOINCREMENT))')

# Create the sensors table if it does not already exist
with db:
    db.execute('CREATE TABLE IF NOT EXISTS "sensors" ("sensorID" INTEGER NOT '
               'NULL UNIQUE, "type" TEXT NOT NULL, "zone" TEXT NOT NULL, '
               'PRIMARY KEY("sensorID" AUTOINCREMENT))')

# Dummy data
data = [("door", "kitchen"),
        ("temperature", "kitchen"),
        ("door", "garage"),
        ("motion", "garage"),
        ("temperature", "garage")]

# Write dummy data to database
with db:
    db.executemany('INSERT INTO "sensors" ("type", "zone") VALUES (?, ?)', data)

# Print out all of the sensors in the kitchen
print("Sensors in kitchen:")
for row in db.execute('SELECT "sensorID", "type" FROM "sensors" WHERE "zone" '
                      '== "kitchen"'):
    print(f"\t{row[0]} ({row[1]})")

print("Door sensors:")
for row in db.execute('SELECT "sensorID", "zone" FROM "sensors" WHERE "type" '
                      '== "door"'):
    print(f"\t{row[0]} ({row[1]})")

# Close the database connection
db.close()

