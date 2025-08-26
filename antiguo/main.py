# main.py
import sys
import sqlite3

#import desde la clase PyQt6 todo lo necesario para lo grafico
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QInputDialog, QMessageBox
)
from PyQt6.QtGui import QFont

from db import obtener_datos_alumno  # función que vas a crear en db.py
from informe_window import InformesWindow

class crear_tabla:
    def __init__(self):
        pass

class MainWindow(QMainWindow):
    
    #constructor de la clase MainWindow
    #inicializa la ventana principal y su diseño
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setFixedSize(600, 400)
        self.init_ui()

    # Método para inicializar la interfaz de usuario
    # Crea los botones y etiquetas, y define su disposición
    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        titulo = QLabel("Menú Principal")
        titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        titulo.setStyleSheet("color: white; background-color: #444; padding: 10px")
        layout.addWidget(titulo)

        self.setLayout(layout)

        # Lista de botones con sus respectivas funciones
        # Cada botón tiene un texto y una función asociada que se ejecuta al hacer clic
        botones = [
            ("Ver Datos Personales", self.ver_datos_personales),
            ("Modificar Datos Personales", self.modificar_datos_personales),
            ("Agregar Nuevo Alumno", self.agregar_nuevo_alumno),
            ("Agregar Nuevas Graduaciones", self.agregar_graduacion),
            ("Asistencia", self.ver_asistencia),
            ("Ver Informes", self.ver_informes)
        ]

        # Itera sobre la lista de botones, creando un QPushButton para cada uno
        # y conectando su clic a la función correspondiente
        for texto, funcion in botones:
            btn = QPushButton(texto)
            btn.setStyleSheet("padding: 10px; font-size: 14px;")
            btn.clicked.connect(funcion)
            layout.addWidget(btn)
        
        crear_tabla()  # Asegúrate de que esta función esté definida en db.py
        
            
        # Configura el widget central de la ventana principal
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # Métodos para cada acción del menú
    # Cada uno de estos métodos se ejecuta al hacer clic en el botón correspondiente
    def ver_datos_personales(self):
        dni, ok = QInputDialog.getText(self, "Buscar Alumno", "Ingresá DNI del alumno:")
        if ok and dni:
            alumno = obtener_datos_alumno(dni)
            if alumno:
                QMessageBox.information(self, "Datos del Alumno", f"{alumno}")
            else:
                QMessageBox.warning(self, "No encontrado", "Alumno no encontrado.")

    def modificar_datos_personales(self):
        # Podés reutilizar ver_datos_personales y abrir AlumnoForm
        pass

    def agregar_nuevo_alumno(self):
        # Aca llamás a AlumnoForm en modo "nuevo"
        pass

    def agregar_graduacion(self):
        pass

    def ver_asistencia(self):
        pass

    def ver_informes(self):
        self.ventana_informes = InformesWindow()
        self.ventana_informes.show()
        # Aca llamás a InformesWindow para ver informes
        
    def crear_tabla():
        conn = sqlite3.connect("alumnos.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT,
                direccion TEXT,
                telefono TEXT,
                email TEXT,
                fecha_nacimiento TEXT,
                grado TEXT,
                observaciones TEXT
            )
        """)
        conn.commit()
        conn.close()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
