import sqlite3

# Warning: This file is created in the current directory
con = sqlite3.connect('backup_info.db')

# Gets updated when items are inserted into backup_repository
con.execute("""
CREATE TABLE backup_info(
id INTEGER PRIMARY KEY,
bup_id INTEGER NOT NULL,
path TEXT NOT NULL,
date TEXT NOT NULL,
time TEXT NOT NULL
)""")

# Gets updated when user creates a regular backup
con.execute("""
CREATE TABLE backup_schedule(
bup_id INTEGER NOT NULL,
day_of_week TEXT NOT NULL,
time TEXT NOT NULL,
weekly BOOLEAN NOT NULL,
monthly BOOLEAN NOT NULL,
yearly BOOLEAN NOT NULL
)""")

con.commit()
