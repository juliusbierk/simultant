import sqlite3
import json

conn = sqlite3.connect('db.sqlite')  # Use absolute paths!
c = conn.cursor()

### DATA ###

def create_dataset(name, content):
    c.execute("REPLACE INTO data VALUES (?, ?)", (name, json.dumps(content)))
    conn.commit()

def get_data_names():
    return [x[0] for x in c.execute("SELECT name FROM data").fetchall()]

def get_data_content(name):
    a = c.execute("SELECT content FROM data WHERE name=?", (name, )).fetchone()
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
