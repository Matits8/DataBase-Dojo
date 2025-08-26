import sys
import sqlite3
import os

#Del paquete PyQt6.Witgets importamos las clases necesarios
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, QScrollArea
)
# Del paquete PyQt6.QtGui importamos las clases necesarios
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from GUIs.alumno_form2 import AlumnoForm  
from GUIs.MenuPrincipal import MenuPrincipal

# Nombre de la base de datos
DB_NAME = "dojo.db"

# Clase principal de la ventana
# Esta clase hereda de QMainWindow, que es la ventana principal de la aplicación
class MainWindow(QMainWindow):
    #Constructor de la ventana principal
    def __init__(self):
        # Llama al constructor de la clase base
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setFixedSize(1600, 1000)
        self.setStyleSheet("background-color: white;")
        
        # Crea un widget central y establece su layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        crear_base_datos()  # Se asegura de crear la DB al iniciar

        self.mostrar_menu_principal()  # <-- ESTA LÍNEA ES IMPORTANTE

    def mostrar_menu_principal(self):
        # Limpia el widget central y establece un nuevo layout
        layout = QVBoxLayout()
        reemplazar_layout(self.central_widget, layout)
        #self.central_widget.setLayout(layout)

        # Encabezado
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #333333;")
        header_layout = QVBoxLayout()
        header.setLayout(header_layout)

        title = QLabel("Menú Principal")
        title.setStyleSheet("color: white;")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(title)
        layout.addWidget(header)

        # Botones
        botones = [
            ("Ver Datos Personales", self.no_implementado),
            ("Modificar Datos Personales", self.no_implementado),
            ("Agregar Nuevo Alumno", self.mostrar_agregar_alumno),
            ("Agregar Nuevas Graduaciones", self.no_implementado),
            ("Asistencia", self.no_implementado),
            ("Ver Informes", self.no_implementado)
        ]
        
        for texto, funcion in botones:
            boton = QPushButton(texto)
            boton.setFixedHeight(40)
            boton.setStyleSheet("""
                QPushButton {
                    background-color: #f2f2f2;
                    font-size: 14px;
                    border: 1px solid #ccc;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
            """)
            boton.clicked.connect(funcion)
            layout.addWidget(boton)

    def mostrar_agregar_alumno(self):
        formulario = AlumnoForm(volver_callback=self.mostrar_menu_principal)
        reemplazar_layout(self.central_widget, formulario.layout())

    def no_implementado(self):
        QMessageBox.information(self, "Aviso", "Esta función aún no está implementada.")


# ✅ Creación inicial de la base de datos
def crear_base_datos():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE alumnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT NOT NULL UNIQUE,
                domicilio TEXT NOT NULL,
                telefono1 TEXT NOT NULL,
                telefono2 TEXT,
                lugar_nacimiento TEXT,
                fecha_nacimiento TEXT NOT NULL,
                ocupacion TEXT NOT NULL,
                estado_civil TEXT NOT NULL,
                practica_actualmente TEXT NOT NULL,
                fecha_ingreso TEXT NOT NULL,
                cinturon TEXT NOT NULL,
                observaciones TEXT,
                edad INTEGER,
                tiempo_practica INTEGER
            )
        """)

        conn.commit()
        conn.close()
        print("✅ Base de datos creada correctamente.")
        
def reemplazar_layout(widget, nuevo_layout):
    layout_antiguo = widget.layout()
    if layout_antiguo is not None:
        while layout_antiguo.count():
            item = layout_antiguo.takeAt(0)
            widget_to_remove = item.widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        QWidget().setLayout(layout_antiguo)
    widget.setLayout(nuevo_layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    menuPrincipal = MenuPrincipal()
    #window = MainWindow()
    #window.show()
    sys.exit(app.exec())
