import sqlite3

conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

### DATA ###

def create_dataset(name, content):
    c.execute("INSERT INTO data VALUES (?, ?)", (name, content))
    conn.commit()

def get_data_names():
    return c.execute("SELECT name FROM data").fetchall()

def get_data_content(name):
    a = c.execute("SELECT content FROM data WHERE name=?", (name, )).fetchone()
    if a is not None:
        return a[0]


### MODELS ###

def create_model(name, content):
    c.execute("INSERT INTO models VALUES (?, ?)", (name, content))
    conn.commit()

def get_models_names():
    return c.execute("SELECT name FROM models").fetchall()

def get_models_content(name):
    a = c.execute("SELECT content FROM models WHERE name=?", (name, )).fetchone()
    if a is not None:
        return a[0]



if __name__ == '__main__':
    print(get_data_names())
    print(get_data_content('test'))



