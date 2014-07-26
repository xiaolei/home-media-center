import sqlite3, logging, os
from flask import g, current_app

DB_UPGRADE_FILE_NAME_PATTERN = 'upgrade_db_from_version{0}to{1}.sql'

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
            sql = f.read()
        db.cursor().executescript(sql)
        db.commit()

def upgrade_db():
    db = get_db()
    current_version = get_db_version()
    new_version = current_version + 1
    filename = os.path.join(current_app.root_path, 'upgrade_db', DB_UPGRADE_FILE_NAME_PATTERN.format(current_version, new_version))
    if os.path.isfile(filename):
        with current_app.open_resource(filename, mode='r') as f:
            sql = f.read()
        if sql:
            db.cursor().executescript(sql)
            if current_version == 0:
                db.execute('insert into settings(key, value) values(?, ?)', ['version', new_version])
            else:
                db.execute('update settings set value=? where key=?', [new_version, 'version'])
            db.commit()
            return new_version
    return current_version

def has_db_update():
    current_version = get_db_version()
    new_version = current_version + 1
    filename = os.path.join(current_app.root_path, 'upgrade_db', DB_UPGRADE_FILE_NAME_PATTERN.format(current_version, new_version))
    return os.path.isfile(filename)

def get_db_version():
    db = get_db()
    sql = "select * from sqlite_master where tbl_name = 'settings' and type = 'table'"
    result = query_db(sql, one=True)
    if result:
        sql = "select value from settings where key = 'version'"
        result = query_db(query=sql, one=True)
        return int(result['value']) if result else 0
    return 0

def execute_sql(sql, args=()):
    db = get_db()
    db.execute(sql, args)
    db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

