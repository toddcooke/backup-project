import sqlite3

# Warning: This file is created in the current directory
con = sqlite3.connect('backup_info.db')

con.execute("""
CREATE TABLE backup_info(
id INTEGER PRIMARY KEY,
action TEXT NOT NULL,
item TEXT NOT NULL,
date TEXT NOT NULL,
time TEXT NOT NULL,
present BOOLEAN NOT NULL
)""")

con.execute("INSERT INTO backup_info VALUES (NULL)")

con.commit()
