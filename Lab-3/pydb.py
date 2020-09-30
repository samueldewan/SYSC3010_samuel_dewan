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

# Insert some dummy data into the database
with db:
    for i in range(10):
        db.execute('INSERT INTO "temperature" ("tempfloat", "datetext") VALUES '
                   '(?, ?)', ((i + 1) * 1.1, datetime.now().isoformat()))

# Read back the data
for row in db.execute('SELECT "id", "tempfloat", "datetext" FROM '
                      '"temperature"'):
    print(f"id: {row[0]}, temp: {row[1]}, date: {row[2]}")

# Close the database connection
db.close()

