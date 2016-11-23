#!/usr/bin/python

import os
import sqlite3
import threading
from bottle import route, run, template, request, static_file, error
from scheduler import backup_service, db_backup_info, db_backup_schedule
from makeDB import make_db

make_db()


@route('/view_backups.html')
def view_backups():
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    c.execute("SELECT * FROM {}".format(db_backup_info))
    select_info = c.fetchall()

    c.execute("SELECT * FROM {}".format(db_backup_schedule))
    select_schedule = c.fetchall()

    c.close()
    return template('html/view_backups', DB_info=select_info, DB_schedule=select_schedule)


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


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


if __name__ == '__main__':
    # # print today - today
    # print datetime.datetime.today() + datetime.timedelta(days=1)
    # print (datetime.datetime.today() - datetime.datetime.today()).days
    #
    # exit()

    threading.Thread(target=backup_service).start()

    # Start bottle server with debugging enabled
    run(debug=True)
