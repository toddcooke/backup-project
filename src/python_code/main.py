#!/usr/bin/env python2.7

import os
import sqlite3
import threading
from bottle import route, run, template, request, static_file, error
from scheduler import backup_service, db_backup_info, db_backup_schedule, \
    copy_item_from_repo, backup_repository, stamp_sep
from makeDB import make_db


def select_all_info():
    pass


def select_all_schedule():
    pass


@route('/view_backups.html')
def view_backups():
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    c.execute("SELECT * FROM {}".format(db_backup_info))
    select_info = c.fetchall()

    c.execute("SELECT * FROM {}".format(db_backup_schedule))
    select_schedule = c.fetchall()

    conn.close()
    return template('html/view_backups', DB_info=select_info, DB_schedule=select_schedule)


@route('/manage_backups.html', method='GET')
def manage_backups():
    restore_id = request.GET.restore.strip()
    delete_id = request.GET.delete.strip()
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    c.execute("SELECT * FROM {}".format(db_backup_info))
    select_info = c.fetchall()

    c.execute("SELECT * FROM {}".format(db_backup_schedule))
    select_schedule = c.fetchall()

    result = template('html/manage_backups', DB_info=select_info, DB_schedule=select_schedule)

    if restore_id:
        bup_id, src, bup_date = c.execute(
            "SELECT bup_id, path, bup_date FROM {} WHERE id = ?".format(db_backup_info), restore_id).fetchone()

        copy_item_from_repo(os.path.join(backup_repository,
                                         os.path.basename(src) + stamp_sep + bup_date + stamp_sep + str(bup_id)), src)

        result = template('html/manage_backups', DB_info=select_info, DB_schedule=select_schedule,
                          msg='Item ' + src + ', backed up on ' + bup_date + ', has been restored.')

    elif delete_id:
        pathname = c.execute('SELECT * FROM {} WHERE bup_id = ?'.format(db_backup_schedule), delete_id).fetchone()[1]
        c.execute('DELETE FROM {} WHERE bup_id = ?'.format(db_backup_info), delete_id)
        c.execute('DELETE FROM {} WHERE bup_id = ?'.format(db_backup_schedule), delete_id)
        conn.commit()
        c.execute("SELECT * FROM {}".format(db_backup_info))
        select_info = c.fetchall()

        c.execute("SELECT * FROM {}".format(db_backup_schedule))
        select_schedule = c.fetchall()
        result = template('html/manage_backups', DB_info=select_info, DB_schedule=select_schedule,
                          msg='The entry: ' + pathname + ' has been removed.')

    conn.close()
    return result


@route('/schedule_backup', method='GET')
def schedule_backup():
    path = request.GET.file_path.strip()
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()
    req = request.GET
    date = req.date.strip()

    c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(db_backup_schedule),
              (None, path, req.offset.strip(), date))
    conn.commit()

    result = template('html/schedule_backup', msg='Successfully scheduled backup of: ' + path)

    if not os.path.exists(path):
        result = template('html/schedule_backup',
                          msg='Error: The path specified was invalid.', msg_type='warning')

    conn.close()
    return result


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
    # Make the db and tables if not already created
    make_db()

    # Start the backup service in the background
    threading.Thread(target=backup_service).start()

    # Start bottle server with debugging enabled
    run(host='127.0.0.1', port=8080, debug=True)
