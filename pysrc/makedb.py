import sqlite3
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(dir_path + '/db.sqlite')
c = conn.cursor()

try:
    c.execute('DROP TABLE data')
    c.execute('DROP TABLE models')
    c.execute('DROP TABLE fits')
except sqlite3.OperationalError:
    pass


conn.commit()

c.execute('CREATE TABLE data (id text, name text, parent text, info text, content text, PRIMARY KEY (id))')
c.execute('CREATE TABLE models (name text, content text, PRIMARY KEY (name))')
c.execute('CREATE TABLE fits (name text, content text, PRIMARY KEY (name))')

conn.commit()
