# Code below kept only for example

@route('/todo')
def todo_list():
    conn = sqlite3.connect('backup_info.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    conn.close()

    output = template('make_table', rows=result)
    return output


@route('/new', method='GET')
def new_item():
    if request.GET.save:

        new = request.GET.task.strip()
        conn = sqlite3.connect('backup_info.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new, 1))
        new_id = c.lastrowid

        conn.commit()
        conn.close()

        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id

    else:
        return template('new_task.tpl')


@route('/edit/<no:int>', method='GET')
def edit_item(no):
    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('backup_info.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('backup_info.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('edit_task', old=cur_data, no=no)


@route('/item<item:re:[0-9]+>')
def show_item(item):
    conn = sqlite3.connect('backup_info.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (item,))
    result = c.fetchall()
    conn.close()

    if not result:
        return 'This item number does not exist!'
    else:
        return 'Task: %s' % result[0]


@route('/help')
def help():
    static_file('help.html', root='.')


@route('/json<json:re:[0-9]+>')
def show_json(json):
    conn = sqlite3.connect('backup_info.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (json,))
    result = c.fetchall()
    conn.close()

    if not result:
        return {'task': 'This item number does not exist!'}
    else:
        return {'task': result[0]}


@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'
