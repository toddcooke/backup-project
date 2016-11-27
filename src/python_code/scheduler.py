import time
import sqlite3
import datetime
import os
import shutil

date_format = "%Y-%m-%d"
db_backup_info = 'backup_info'
db_backup_schedule = 'backup_schedule'
backup_repository = 'backup_repository'
stamp_sep = '.'


def copy_item_to_repo(src, stamp, id):
    """
    Copies a file or dir to the bup repo
    :param src: The item to copy
    :param stamp: A timestamp which is today's date in fmt yyyy-mm-dd
    :param id: The bup id of the item to copy
    """
    basename = os.path.basename(src)
    stamp = stamp_sep + stamp + stamp_sep + str(id)
    if os.path.isfile(src):
        shutil.copy2(src, os.path.join(backup_repository, basename + stamp))
    elif os.path.isdir(src):
        shutil.copytree(src, os.path.join(backup_repository, os.path.basename(src) + stamp))
    else:
        # TODO handle case where item is in DB_info but not filesystem
        pass


def copy_item_from_repo(src, dest):
    """
    Copies an file or dir from the the bup repo to its original location
    :param src: The item to copy
    :param dest: The original location of the item
    """
    if os.path.isfile(src):
        shutil.copy2(src, dest)
    elif os.path.isdir(src):
        # Must delete existing dir before creating new one
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    else:
        # TODO handle case where items are in DB_info but not in bup repo
        pass


def str_to_date(s):
    """
    :param s: s in format yyyy-mm-dd
    :return: s in datetime format
    """
    s = [int(i) for i in s.split('-')]
    return datetime.date(s[0], s[1], s[2])


def backup_service():
    """
    Read DB, if today is day for a backup, run backup
    """
    while not time.sleep(60):

        today = datetime.date.today()

        conn = sqlite3.connect(db_backup_info + '.db')
        c = conn.cursor()

        c.execute("SELECT * FROM {}".format(db_backup_schedule))
        select_schedule = c.fetchall()

        c.execute("SELECT * FROM {}".format(db_backup_info))
        select_info = c.fetchall()

        for count, entry in enumerate(select_schedule):
            bup_id, path, offset, schedule_date = entry
            # path = entry[1]
            # offset = entry[2]
            # schedule_date = entry[3]

            already_in = c.execute(
                "SELECT * FROM {} WHERE bup_id = ? AND path = ? AND bup_date = ?".format(db_backup_info),
                (bup_id, path, today)).fetchone()

            # if item was not already backed up today or if db_info is not populated
            if not select_info or not already_in:
                # if today is the day to backup
                if (str_to_date(schedule_date) - today).days % int(offset) == 0:
                    # backup this path to backup repo
                    copy_item_to_repo(path, str(today), bup_id)
                    # make entry in db_info
                    c.execute("INSERT INTO {} VALUES (?,?,?,?,?)".format(db_backup_info),
                              (None, entry[0], entry[1], entry[2], str(today)))
                    conn.commit()

        c.close()
