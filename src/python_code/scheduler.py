import time
import sqlite3
import datetime
import os
import shutil

date_format = "%Y-%m-%d"
db_backup_info = 'backup_info'
db_backup_schedule = 'backup_schedule'
backup_repository = 'backup_repository'


def copy_item_to_repo(item):
    if os.path.isfile(item):
        shutil.copy2(item, backup_repository + os.path.sep)
    else:
        shutil.copytree(item, backup_repository + os.path.sep + os.path.basename(item))


def copy_item_from_repo(item):
    pass


def backup_service():
    """
    Read DB, if today is day for a backup, run backup
    """
    while True:
        time.sleep(60)

        today = datetime.date.today()

        conn = sqlite3.connect(db_backup_info + '.db')
        c = conn.cursor()

        c.execute("SELECT * FROM {}".format(db_backup_schedule))
        select_schedule = c.fetchall()

        c.execute("SELECT * FROM {}".format(db_backup_info))
        select_info = c.fetchall()

        for count, entry in enumerate(select_schedule):
            path = entry[1]
            offset = entry[2]
            schedule_date = entry[3]

            # if item was not already backed up today or if db_info is not populated
            if not select_info or str_to_date(select_info[count][-1]) != today:
                # if today is the day to backup
                if (str_to_date(schedule_date) - today).days % int(offset) == 0:
                    # backup this path to backup repo
                    copy_item_to_repo(path)
                    # make entry in db_info
                    c.execute("INSERT INTO {} VALUES (?,?,?,?,?)".format(db_backup_info),
                              (None, entry[0], entry[1], entry[2], entry[3]))
                    conn.commit()

        c.close()


def str_to_date(s):
    """
    :param s: s in format yyyy-mm-dd
    :return: s in datetime format
    """
    s = [int(i) for i in s.split('-')]
    return datetime.date(s[0], s[1], s[2])
