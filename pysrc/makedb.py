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

c.execute('CREATE TABLE data (name text, content text)')
c.execute('CREATE TABLE models (name text, content text)')
c.execute('CREATE TABLE fits (name text, content text)')

conn.commit()
