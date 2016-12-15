import sqlite3
from scheduler import db_backup_info, db_backup_schedule


def make_db():
    # Warning: This file is created in the current directory
    con = sqlite3.connect('backup_info.db')

    # Gets updated when items are inserted into backup_repository
    con.execute("""
    CREATE TABLE IF NOT EXISTS {}(
    id INTEGER PRIMARY KEY,
    bup_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    offset INTEGER NOT NULL,
    bup_date TEXT NOT NULL
    )""".format(db_backup_info))

    # Gets updated when user schedules a regular backup
    # Offset should be one of weekly, monthly, or yearly
    con.execute("""
    CREATE TABLE IF NOT EXISTS {}(
    bup_id INTEGER PRIMARY KEY,
    path TEXT NOT NULL,
    offset INTEGER NOT NULL,
    schedule_date TEXT NOT NULL
    )""".format(db_backup_schedule))

    con.commit()
