import os
import shutil
import sqlite3
from sqlite3 import OperationalError
from bottle import route, run, debug, template, request, static_file, error

db_name = 'backup_info'
backup_repository = 'backup_repository'


def database_query(query):
    conn = sqlite3.connect(db_name + '.db')
    c = conn.cursor()

    try:
        c.execute(query)
    except OperationalError as e:
        return ['error', 'Query returned an error: ', e]

    result = c.fetchall()
    c.close()
    return result


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')


@route('/')
def main_page():
    return template('html/index', msg='')


@route('/create_recovery_media')
def main_page():
    return template('html/create_recovery_media', msg='')


@route('/create_backup', method='GET')
def new_item():
    path = request.GET.file_path.strip()
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

    # Backup and make entry in DB
    if os.path.exists(path):
        if os.path.isfile(path):
            shutil.copy2(path, backup_repository + os.path.sep)
        else:
            shutil.copytree(path, backup_repository + os.path.sep + os.path.basename(path))
            # database_query('INSERT INTO {} VALUES ({},{},{},{},{})'
            #                .format(db_name,None,path,request.GET.))
        return template('html/regular_backup', msg='Item backed up successfully.')
    # Return to body with error message
    else:
        return template('html/regular_backup', msg='Error: The path specified was invalid.')


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


# Start bottle server with debugging enabled
debug(True)
run()
