import sqlite3

DB_NAME = "database/dojo.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

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

def obtener_todos_los_alumnos():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, apellido, nombre FROM alumnos")
    alumnos = cursor.fetchall()
    conn.close()
    return alumnos

def obtener_alumno_por_id(alumno_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos WHERE id = ?", (alumno_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "dni": row[3],
            "cinturon": row[4],
            "fecha_inicio": row[5],
            "tiempo_practica": row[6],
            "examenes": row[7],
            "observaciones": row[8],
        }
    return None

def agregar_alumno(alumno):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alumnos (nombre, apellido, dni, cinturon, fecha_inicio, tiempo_practica, examenes, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        alumno["nombre"], alumno["apellido"], alumno["dni"],
        alumno["cinturon"], alumno["fecha_inicio"],
        int(alumno["tiempo_practica"]) if alumno["tiempo_practica"].isdigit() else 0,
        alumno["examenes"], alumno["observaciones"]
    ))
    conn.commit()
    conn.close()

def editar_alumno(alumno):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE alumnos
        SET nombre = ?, apellido = ?, dni = ?, cinturon = ?, fecha_inicio = ?, tiempo_practica = ?, examenes = ?, observaciones = ?
        WHERE id = ?
    """, (
        alumno["nombre"], alumno["apellido"], alumno["dni"],
        alumno["cinturon"], alumno["fecha_inicio"],
        int(alumno["tiempo_practica"]) if alumno["tiempo_practica"].isdigit() else 0,
        alumno["examenes"], alumno["observaciones"],
        alumno["id"]
    ))
    conn.commit()
    conn.close()

def eliminar_alumno(alumno_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumnos WHERE id = ?", (alumno_id,))
    conn.commit()
    conn.close()

def obtener_datos_alumno(dni):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos WHERE dni = ?", (dni,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        columnas = [col[0] for col in cursor.description]
        return dict(zip(columnas, resultado))
    return None

def buscar_alumnos(filtro):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumnos WHERE nombre LIKE ? OR apellido LIKE ?", (f"%{filtro}%", f"%{filtro}%"))
    resultados = cursor.fetchall()
    conn.close()
    return [
        {
            "id": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "dni": row[3],
            "cinturon": row[4],
            "fecha_inicio": row[5],
            "tiempo_practica": row[6],
            "examenes": row[7],
            "observaciones": row[8]
        } for row in resultados
    ]