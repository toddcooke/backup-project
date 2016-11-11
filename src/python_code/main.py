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
    return template('html/index', msg='')


@route('/restore_backup.html', method='GET')
def restore_backup():
    path = request.GET.file_path.strip()

    # if not path:
    #     return template('html/restore_backup', msg='')

    select = database_query("select * from {}".format(db_backup_schedule))
    # if select[0] == 'error':
    #     return template('html/restore_backup', msg='Error: ' + select[-1])
    return template('html/restore_backup', msg=select)


@route('/<item>.html')
def regular_backup(item):
    return template('html/{}'.format(item), msg='')


def database_query(query, values):
    conn = sqlite3.connect(db_backup_info + '.db')
    c = conn.cursor()

    TEST = (None,
            '/home/todd/ok.txt',
            'montue',
            '15:30',
            1,
            0,
            0)

    try:
        c.execute(query, TEST)
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
    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    path = request.GET.file_path.strip()

    if not os.path.exists(path):
        return template('html/schedule_{}_backup'.format(kind), msg='Error: The path specified was invalid.')

    if kind == 'weekly':
        checked_days = '_'.join([i for i in request.query.keys() if i in days])
        result = database_query('INSERT INTO {} VALUES (?,?,?,?,?,?,?)'.format(db_backup_schedule),
                                (None, path, checked_days, request.GET.time.strip(),
                                 True, False, False))

        return template('html/schedule_{}_backup'.format(kind), msg=result)
    elif kind == 'monthly':
        pass
    elif kind == 'custom':
        pass
    else:
        pass


@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


# Start bottle server with debugging enabled
run(debug=True)
