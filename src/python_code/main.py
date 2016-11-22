#!/usr/bin/python

import os
import shutil
import sqlite3
import datetime
from bottle import route, run, template, request, static_file, error


def str_to_date(s):
    """
    :param s: s in format yyyy-mm-dd
    :return: s in datetime format
    """
    return datetime.datetime.strptime(s, date_format)


def date_to_str(d):
    """
    :param d:
    :return: d in a string format
    """
    return d.strftime(date_format)


def add_x_days(d, x):
    """
    :param d: datetime object
    :param x: integer, number of days to increment
    :return: d incremented by x days
    """
    return d + datetime.timedelta(days=x)


@route('/view_backups.html', method='GET')
def view_backups():
    path = request.GET.file_path.strip()
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    c.execute("SELECT * FROM {}".format(db_backup_info))
    select_info = c.fetchall()

    c.execute("SELECT * FROM {}".format(db_backup_schedule))
    select_schedule = c.fetchall()

    # If user has not hit submit yet
    if not path:
        result = template('html/view_backups', DB_info=select_info, DB_schedule=select_schedule)

    else:
        if not select_info:
            result = template('html/view_backups',
                              msg='Error: There are no backups to restore',
                              msg_type='warning', DB_info=select_info, DB_schedule=select_schedule)
        else:
            result = template('html/view_backups', msg=select_info, DB_info=select_info, DB_schedule=select_schedule)

    # If backup_info table is empty
    if not select_info:
        result = template('html/view_backups', msg='Nothing has been backed up yet!', DB_info=select_info,
                          DB_schedule=select_schedule)

    c.close()
    return result


@route('/schedule_backup', method='GET')
def schedule_backup():
    path = request.GET.file_path.strip()
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()
    req = request.GET

    c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(db_backup_schedule),
              (None, path, req.offset.strip(), req.date.strip()))
    conn.commit()

    result = template('html/schedule_backup', msg='Successfully scheduled backup of: ' + path)

    if not os.path.exists(path):
        result = template('html/schedule_backup',
                          msg='Error: The path specified was invalid.', msg_type='warning')

    c.close()
    return result


@route('/restore_backup.html', method='GET')
def restore_backup():
    path = request.GET.file_path.strip()
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    c.execute("SELECT * FROM {}".format(db_backup_info))
    select_schedule = c.fetchall()

    # If backup_info table is empty
    if not select_schedule:
        return template('html/restore_backup', msg='Nothing has been backed up yet!', DB_info=select_schedule)

    # If user has not hit submit yet
    if not path:
        c.close()
        return template('html/restore_backup', DB_info=select_schedule)

    else:
        c.execute("SELECT * FROM {}".format(db_backup_info))
        select_schedule = c.fetchall()
        c.close()
        if not select_schedule:
            return template('html/restore_backup',
                            msg='Error: There are no backups to restore', msg_type='warning', DB_info=select_schedule)
        return template('html/restore_backup', msg=select_schedule, DB_info=select_schedule)


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')


@route('/')
def main_page():
    return template('html/index')


@route('/<item>.html')
def any_html(item):
    return template('html/{}'.format(item))


def copy_item_to_repo(item):
    if os.path.isfile(item):
        shutil.copy2(item, backup_repository + os.path.sep)
    else:
        shutil.copytree(item, backup_repository + os.path.sep + os.path.basename(item))


def copy_item_from_repo(item):
    pass


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


db_backup_info = 'backup_info'
db_backup_schedule = 'backup_schedule'
backup_repository = 'backup_repository'
date_format = "%Y-%m-%d"
# today = date_to_str(datetime.datetime.today())

if __name__ == '__main__':
    # Start bottle server with debugging enabled
    run(debug=True)
