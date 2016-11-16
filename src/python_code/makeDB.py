import sqlite3

# Warning: This file is created in the current directory
con = sqlite3.connect('backup_info.db')

# Gets updated when items are inserted into backup_repository
con.execute("""
CREATE TABLE IF NOT EXISTS backup_info(
id INTEGER PRIMARY KEY,
bup_id INTEGER NOT NULL,
path TEXT NOT NULL,
bup_date TEXT NOT NULL,
bup_time TEXT NOT NULL
)""")

# Gets updated when user creates a regular backup
# Frequency should be one of weekly, monthly, or yearly
con.execute("""
CREATE TABLE IF NOT EXISTS backup_schedule(
bup_id INTEGER PRIMARY KEY,
path TEXT NOT NULL,
day_of_week TEXT NOT NULL,
frequency TEXT NOT NULL,
bup_time TEXT NOT NULL
)""")

con.commit()


"""
insert into backup_schedule values(
NULL,
'/home/todd/ok.txt',
'montue',
'15:30',
1,
0,
0)
"""