import sqlite3
from flask import g

DATABASE = 'database.db'

def get_db(app=None):
    if app:
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row
        return db
    else:
        raise RuntimeError("Flask application not provided.")

def init_db(app):
    with app.app_context():
        db = get_db(app)
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

