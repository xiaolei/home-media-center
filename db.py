import sqlite3, logging
from flask import g, current_app

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE_URI'])
        db.row_factory = make_dicts
        db.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    return db

def create_db():
    with current_app.app_context():
        db = get_db()
        sql = ''
        with current_app.open_resource('database.sql', mode='r') as f:
            sql = f.read();
            db.cursor().executescript(sql)
        db.commit()

def execute_sql(sql, args=()):
    db = get_db()
    db.execute(sql, args)
    db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
