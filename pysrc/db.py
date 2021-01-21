import sqlite3
import json
from collections import defaultdict
from uuid import uuid4

conn = sqlite3.connect('db.sqlite')  # Use absolute paths!
c = conn.cursor()

### DATA ###

def create_dataset(name, parent, content):
    info = f'{len(content["x"])} datapoints'
    c.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?)", (str(uuid4()), name, parent, info, json.dumps(content)))
    conn.commit()

def get_data_names():
    d = defaultdict(list)
    for x in c.execute("SELECT id, name, parent, info FROM data").fetchall():
        d[x[2]].append({'name': x[1], 'id': x[0], 'info': x[3]})
    return dict(d)


def get_data_content(ID):
    a = c.execute("SELECT content FROM data WHERE id=?", (ID, )).fetchone()
    if a is not None:
        return json.loads(a[0])


### MODELS ###

def create_model(name, content):
    c.execute("REPLACE INTO models VALUES (?, ?)", (name, json.dumps(content)))
    conn.commit()

def get_models_names():
    return [x[0] for x in c.execute("SELECT name FROM models").fetchall()]

def get_models_content(name):
    a = c.execute("SELECT content FROM models WHERE name=?", (name, )).fetchone()
    if a is not None:
        return json.loads(a[0])

def get_all_models():
    return {x[0]: json.loads(x[1]) for x in c.execute("SELECT name, content FROM models").fetchall()}



if __name__ == '__main__':
    print(get_models_names())
