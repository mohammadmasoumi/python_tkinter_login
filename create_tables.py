import sqlite3

conn = sqlite3.connect('example.db')
cur = conn.cursor()

cur.execute(
    '''CREATE TABLE users (firstname text, lastname text, username text, password text, gender real, country real, language real)''')
