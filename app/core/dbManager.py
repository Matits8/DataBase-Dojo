import sqlite3
import os
from datetime import datetime

DB_FILE = "dojo.sqlite"

def crear_base_datos():
    #Consulta si no existe la base de datos y la crea si no existe
    if not os.path.exists(DB_FILE):
        # Crea la conexión a la base de datos
        try:
            with sqlite3.connect(DB_FILE) as conn:
                # Crea un cursor para ejecutar comandos SQL
                c = conn.cursor()
                # Crea la tabla de alumnos si no existe
                c.execute('''
                    CREATE TABLE alumnos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        dni TEXT NOT NULL,
                        domicilio TEXT,
                        telefono1 TEXT NOT NULL,
                        telefono2 TEXT,
                        lugar_nacimiento TEXT,
                        fecha_nacimiento TEXT NOT NULL,
                        ocupacion TEXT,
                        estado_civil TEXT,
                        practica_actualmente TEXT,
                        fecha_ingreso TEXT NOT NULL,
                        cinturon TEXT,
                        observaciones TEXT,
                        edad INTEGER,
                        tiempo_practica TEXT,
                        UNIQUE(nombre, apellido)
                    )
                ''')
                # Guarda los cambios
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la base de datos: {e}")

def alumno_existe(nombre, apellido):
    # Verifica si un alumno con el mismo nombre y apellido ya existe
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute("SELECT 1 FROM alumnos WHERE nombre=? AND apellido=?", (nombre, apellido))
        return c.fetchone() is not None

def calcular_edad(fecha_nac_str):
    # Calcula la edad a partir de la fecha de nacimiento
    fecha_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d").date()
    hoy = datetime.today().date()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

def calcular_tiempo_practica(fecha_ingreso_str):
    # Calcula el tiempo de práctica a partir de la fecha de ingreso
    fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d").date()
    hoy = datetime.today().date()
    años = hoy.year - fecha_ingreso.year
    meses = hoy.month - fecha_ingreso.month
    if hoy.day < fecha_ingreso.day:
        meses -= 1
    if meses < 0:
        años -= 1
        meses += 12
    return f"{años} años, {meses} meses"

def agregar_alumno(data):
    # Agrega un nuevo alumno a la base de datos
    edad = calcular_edad(data["FechaNacimiento"])
    tiempo_practica = calcular_tiempo_practica(data["FechaIngreso"])

    # Verifica si el alumno ya existe
    # Si el alumno ya existe, no lo agrega
    with sqlite3.connect(DB_FILE) as conn:
        # Crea un cursor para ejecutar comandos SQL
        c = conn.cursor()
        c.execute('''
            INSERT INTO alumnos (
                nombre, apellido, dni, domicilio, telefono1, telefono2,
                lugar_nacimiento, fecha_nacimiento, ocupacion, estado_civil,
                practica_actualmente, fecha_ingreso, cinturon, observaciones,
                edad, tiempo_practica
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["Nombre"], data["Apellido"], data["DNI"], data["Domicilio"],
            data["Telefono1"], data["Telefono2"], data["LugarNacimiento"], data["FechaNacimiento"],
            data["Ocupacion"], data["EstadoCivil"], data["PracticaActualmente"],
            data["FechaIngreso"], data["Cinturon"], data["Observaciones"], edad, tiempo_practica
        ))
        conn.commit()
