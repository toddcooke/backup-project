import os
import shutil
import sqlite3
from sqlite3 import OperationalError
from bottle import route, run, debug, template, request, static_file, error

db_name = 'backup_info'
backup_repository = 'backup_repository'
backup_schedule = 'backup_schedule'


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')


@route('/')
def main_page():
    return template('html/index', msg='')


@route('/<item>.html')
def regular_backup(item):
    return template('html/{}'.format(item), msg='')


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


def copy_item_to_repo(item):
    if os.path.isfile(item):
        shutil.copy2(item, backup_repository + os.path.sep)
    else:
        shutil.copytree(item, backup_repository + os.path.sep + os.path.basename(item))


@route('/schedule_<kind>_backup', method='GET')
def new_item(kind):
    path = request.GET.file_path.strip()
    # days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']

    # Backup and make entry in DB
    if os.path.exists(path):
        # database_query('insert into {} VALUES ()')
        return template('html/schedule_{}_backup'.format(kind), msg='Item backed up successfully.')
    # Return to body with error message
    else:
        return template('html/schedule_{}_backup'.format(kind), msg='Error: The path specified was invalid.')


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


# Start bottle server with debugging enabled
debug(True)
run()
