import sqlite3

DB_NAME = "database/dojo.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT UNIQUE,
            cinturon TEXT,
            fecha_inicio TEXT,
            tiempo_practica INTEGER,
            examenes TEXT,
            observaciones TEXT
        )
    ''')
    conn.commit()
    conn.close()
