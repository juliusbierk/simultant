import sqlite3
import json
from collections import defaultdict
from uuid import uuid4
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

conn = sqlite3.connect(dir_path + '/db.sqlite') 
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

def delete_data(parent):
    c.execute("DELETE FROM data WHERE parent=?", (parent, ))
    conn.commit()


### MODELS ###

def create_model(name, content):
    c.execute("REPLACE INTO models VALUES (?, ?)", (name, json.dumps(content)))
    conn.commit()

def delete_model(name):
    c.execute("DELETE FROM models WHERE name=?", (name, ))
    conn.commit()

def get_models_names():
    return [x[0] for x in c.execute("SELECT name FROM models").fetchall()]

def args_to_kwargs(d):
    kwargs = {x['name']: x['value'] for x in d['args']}
    if not d['expr_mode']:
        y0 = kwargs['y0']
        del kwargs['y0']
        for i in range(len(y0)):
            kwargs[f'y0[{i}]'] = y0[i]
    return kwargs


def get_models_content(name):
    a = c.execute("SELECT content FROM models WHERE name=?", (name, )).fetchone()
    if a is not None:
        data = json.loads(a[0])
        data['kwargs'] = args_to_kwargs(data)
        return data

def get_all_models():
    data = {x[0]: json.loads(x[1]) for x in c.execute("SELECT name, content FROM models").fetchall()}
    for m in data:
        data[m]['kwargs'] = args_to_kwargs(data[m])
    return data



if __name__ == '__main__':
    print(get_models_names())
