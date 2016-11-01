import sqlite3

# Check DB if it is time to run backup
conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")

print c.fetchall()
