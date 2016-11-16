#!/usr/bin/python

import os
import shutil
import sqlite3
from sqlite3 import OperationalError
from bottle import route, run, template, request, static_file, error

db_backup_info = 'backup_info'
db_backup_schedule = 'backup_schedule'
backup_repository = 'backup_repository'
msg_success = 'Item backed up successfully'


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')


@route('/')
def main_page():
    return template('html/index')


@route('/restore_backup.html', method='GET')
def restore_backup():
    path = request.GET.file_path.strip()
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    c.execute("SELECT * FROM {}".format(db_backup_schedule))
    select_schedule = c.fetchall()
    c.close()

    # If user has not hit submit yet
    if not path:
        return template('html/restore_backup', DB_info=select_schedule)

    else:
        c.execute("SELECT * FROM {}".format(db_backup_info))
        select_schedule = c.fetchall()
        c.close()
        if not select_schedule:
            return template('html/restore_backup',
                            msg='Error: There are no backups to restore', msg_type='warning', DB_info=select_schedule)
        return template('html/restore_backup', msg=select_schedule, DB_info=select_schedule)


@route('/<item>.html')
def any_html(item):
    return template('html/{}'.format(item))


def copy_item_to_repo(item):
    if os.path.isfile(item):
        shutil.copy2(item, backup_repository + os.path.sep)
    else:
        shutil.copytree(item, backup_repository + os.path.sep + os.path.basename(item))


@route('/schedule_<kind>_backup', method='GET')
def schedule_backup(kind):
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    path = request.GET.file_path.strip()

    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    if not os.path.exists(path):
        return template('html/schedule_{}_backup'.format(kind),
                        msg='Error: The path specified was invalid.', msg_type='warning')

    if kind == 'weekly':
        checked_days = '_'.join([i for i in request.query.keys() if i in days])
        if not checked_days:
            return template('html/schedule_{}_backup'.format(kind),
                            msg='Error: At least one day must be selected.', msg_type='warning')

        c.execute('INSERT INTO {} VALUES (?,?,?,?,?,?,?)'.format(db_backup_schedule),
                  (None, path, checked_days, request.GET.time.strip(), True, False, False))
        c.close()
        conn.commit()

        return template('html/schedule_{}_backup'.format(kind), msg='Successful backup of: ' + path)

    elif kind == 'monthly':
        pass
    elif kind == 'custom':
        pass
    else:
        pass


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


if __name__ == '__main__':
    # Start bottle server with debugging enabled
    run(debug=True)
