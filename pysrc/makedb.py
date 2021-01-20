import sqlite3

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

try:
    c.execute('DROP TABLE data')
    c.execute('DROP TABLE models')
    c.execute('DROP TABLE fits')
except sqlite3.OperationalError:
    pass


conn.commit()

c.execute('CREATE TABLE data (id text, name text, parent text, content text, PRIMARY KEY (id))')
c.execute('CREATE TABLE models (name text, content text, PRIMARY KEY (name))')
c.execute('CREATE TABLE fits (name text, content text, PRIMARY KEY (name))')

conn.commit()
