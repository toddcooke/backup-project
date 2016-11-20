import sqlite3

# Warning: This file is created in the current directory
con = sqlite3.connect('backup_info.db')

# Gets updated when items are inserted into backup_repository
con.execute("""
CREATE TABLE IF NOT EXISTS backup_info(
id INTEGER PRIMARY KEY,
bup_id INTEGER NOT NULL,
path TEXT NOT NULL,
offset INTEGER NOT NULL,
bup_date TEXT NOT NULL
)""")

# Gets updated when user creates a regular backup
# Offset should be one of weekly, monthly, or yearly
con.execute("""
CREATE TABLE IF NOT EXISTS backup_schedule(
bup_id INTEGER PRIMARY KEY,
path TEXT NOT NULL,
offset INTEGER NOT NULL,
bup_date TEXT NOT NULL
)""")

con.commit()

# ex: 7 days = 1 week/ 31 days = 1 month/ 365 days = 1 year/ any other amount is custom
# remove separate backup pages. Have only one and let user specify offset


"""
INSERT INTO backup_schedule VALUES(
NULL,
'/home/todd/ok.txt',
'montue',
'15:30',
1,
0,
0)
"""
