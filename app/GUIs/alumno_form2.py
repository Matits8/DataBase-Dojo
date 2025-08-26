from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QDateEdit, QComboBox,QScrollArea
)
from PyQt6.QtCore import QDate
import sqlite3
import datetime
from core.dbManager import agregar_alumno, alumno_existe


class AlumnoForm(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.callback_volver = volver_callback  # 👈 Esta línea es la clave
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Diccionario para guardar referencias a los campos
        self.campos = {}

        # Lista de campos: (nombre interno, etiqueta, tipo, obligatorio)
        campos_info = [
            ("nombre", "Nombre", "texto", True),
            ("apellido", "Apellido", "texto", True),
            ("dni", "DNI", "texto", True),
            ("domicilio", "Domicilio", "texto", False),
            ("telefono1", "Teléfono 1", "texto", True),
            ("telefono2", "Teléfono 2", "texto", False),
            ("lugar_nacimiento", "Lugar de Nacimiento", "texto", False),
            ("fecha_nacimiento", "Fecha de Nacimiento", "fecha", True),
            ("ocupacion", "Ocupación", "texto", False),
            ("estado_civil", "Estado Civil", "combo", False),
            ("practica_actualmente", "¿Practica Actualmente?", "combo_si_no", False),
            ("fecha_ingreso", "Fecha de Ingreso", "fecha", True),
            ("cinturon", "Cinturón", "texto", False),
            ("observaciones", "Observaciones", "texto_largo", False)
        ]

        for key, label, tipo, obligatorio in campos_info:
            layout.addWidget(QLabel(f"{label}:"))
            if tipo == "texto":
                campo = QLineEdit()
            elif tipo == "texto_largo":
                campo = QTextEdit()
            elif tipo == "fecha":
                campo = QDateEdit()
                campo.setCalendarPopup(True)
                campo.setDate(QDate.currentDate())
            elif tipo == "combo":
                campo = QComboBox()
                campo.addItems(["", "Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"])
            elif tipo == "combo_si_no":
                campo = QComboBox()
                campo.addItems(["", "Sí", "No"])

            self.campos[key] = (campo, obligatorio)
            layout.addWidget(campo)

        # Botones
        btn_layout = QHBoxLayout()
        self.setLayout(layout)
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.callback_volver)
        btn_layout.addWidget(self.btn_guardar)
        btn_layout.addWidget(self.btn_cancelar)
        
        #FECHA
        self.fecha_ingreso = QDateEdit()
        self.fecha_ingreso.setCalendarPopup(True)
        self.fecha_ingreso.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Fecha de Ingreso"))
        layout.addWidget(self.fecha_ingreso)

        self.practica_actualmente = QComboBox()
        self.practica_actualmente.addItems(["Sí", "No"])
        layout.addWidget(QLabel("¿Practica Actualmente?"))
        layout.addWidget(self.practica_actualmente)

        
        
    def limpiar_formulario(self):
        for campo in self.campos.values():
            campo.clear()
        self.fecha_nacimiento.setDate(QDate.currentDate())
        self.fecha_ingreso.setDate(QDate.currentDate())
        self.practica_actualmente.setCurrentIndex(0)
    
    def guardar(self):
        # Verificar campos obligatorios
        obligatorios = ["Nombre", "Apellido", "DNI", "Telefono1"]
        for campo in obligatorios:
            if not self.campos[campo].text().strip():
                QMessageBox.warning(self, "Error", f"El campo '{campo}' es obligatorio.")
                return

        if not self.fecha_nacimiento.date() or not self.fecha_ingreso.date():
            QMessageBox.warning(self, "Error", "Debe ingresar las fechas de nacimiento e ingreso.")
            return

        nombre = self.campos["Nombre"].text().strip()
        apellido = self.campos["Apellido"].text().strip()

        # Chequear si ya existe
        if alumno_existe(nombre, apellido):
            QMessageBox.warning(self, "Error", "Ya existe un alumno con ese nombre y apellido.")
            return

        datos = {
            "Nombre": nombre,
            "Apellido": apellido,
            "DNI": self.campos["DNI"].text().strip(),
            "Domicilio": self.campos["Domicilio"].text().strip(),
            "Telefono1": self.campos["Telefono1"].text().strip(),
            "Telefono2": self.campos["Telefono2"].text().strip(),
            "LugarNacimiento": self.campos["Lugar de Nacimiento"].text().strip(),
            "FechaNacimiento": self.fecha_nacimiento.date().toString("yyyy-MM-dd"),
            "Ocupacion": self.campos["Ocupacion"].text().strip(),
            "EstadoCivil": self.campos["Estado Civil"].text().strip(),
            "PracticaActualmente": self.practica_actualmente.currentText(),
            "FechaIngreso": self.fecha_ingreso.date().toString("yyyy-MM-dd"),
            "Cinturon": self.campos["Cinturon"].text().strip(),
            "Observaciones": self.campos["Observaciones"].text().strip()
        }

        agregar_alumno(datos)
        QMessageBox.information(self, "Éxito", "Alumno guardado correctamente.")
        self.callback_volver()
    
    
    def mostrar_error(self):
        QMessageBox.warning(self, "Faltan Datos", "Debe completar los campos obligatorios.")
        