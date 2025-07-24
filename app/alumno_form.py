from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from app.db import connect_db

class AlumnoForm(QWidget):
    def __init__(self, alumno=None):
        super().__init__()
        self.setWindowTitle("Formulario Alumno")
        self.alumno = alumno  # Si viene con datos para modificar

        # Campos
        self.nombre_input = QLineEdit()
        self.apellido_input = QLineEdit()
        self.dni_input = QLineEdit()
        self.cinturon_input = QComboBox()
        self.cinturon_input.addItems(["Blanco", "Amarillo", "Naranja", "Verde", "Azul", "Marrón", "Negro"])
        self.fecha_inicio_input = QLineEdit()  # Podés mejorar con un DateEdit luego
        self.tiempo_practica_input = QLineEdit()
        self.examenes_input = QTextEdit()
        self.observaciones_input = QTextEdit()

        # Botones
        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.clicked.connect(self.guardar_alumno)

        # Layout
        layout = QVBoxLayout()

        def add_row(label_text, widget):
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            row.addWidget(widget)
            layout.addLayout(row)

        add_row("Nombre:", self.nombre_input)
        add_row("Apellido:", self.apellido_input)
        add_row("DNI:", self.dni_input)
        add_row("Cinturón:", self.cinturon_input)
        add_row("Fecha Inicio:", self.fecha_inicio_input)
        add_row("Tiempo Práctica (meses):", self.tiempo_practica_input)
        add_row("Exámenes:", self.examenes_input)
        add_row("Observaciones:", self.observaciones_input)

        layout.addWidget(self.guardar_btn)
        self.setLayout(layout)

        # Si es modificar, cargar datos
        if alumno:
            self.cargar_datos()

    def cargar_datos(self):
        self.nombre_input.setText(self.alumno.get("nombre", ""))
        self.apellido_input.setText(self.alumno.get("apellido", ""))
        self.dni_input.setText(self.alumno.get("dni", ""))
        cinturon = self.alumno.get("cinturon", "")
        index = self.cinturon_input.findText(cinturon, Qt.MatchFlag.MatchFixedString)
        if index >= 0:
            self.cinturon_input.setCurrentIndex(index)
        self.fecha_inicio_input.setText(self.alumno.get("fecha_inicio", ""))
        self.tiempo_practica_input.setText(str(self.alumno.get("tiempo_practica", "")))
        self.examenes_input.setPlainText(self.alumno.get("examenes", ""))
        self.observaciones_input.setPlainText(self.alumno.get("observaciones", ""))

    def guardar_alumno(self):
        # Validar datos básicos
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        if not nombre or not apellido:
            QMessageBox.warning(self, "Error", "Nombre y Apellido son obligatorios")
            return

        # Guardar en DB
        conn = connect_db()
        cursor = conn.cursor()
        if self.alumno:  # modificar
            cursor.execute('''
                UPDATE alumnos SET nombre=?, apellido=?, dni=?, cinturon=?, fecha_inicio=?, tiempo_practica=?, examenes=?, observaciones=?
                WHERE id=?
            ''', (
                nombre,
                apellido,
                self.dni_input.text().strip(),
                self.cinturon_input.currentText(),
                self.fecha_inicio_input.text().strip(),
                int(self.tiempo_practica_input.text()) if self.tiempo_practica_input.text().isdigit() else 0,
                self.examenes_input.toPlainText(),
                self.observaciones_input.toPlainText(),
                self.alumno["id"]
            ))
        else:  # nuevo
            cursor.execute('''
                INSERT INTO alumnos (nombre, apellido, dni, cinturon, fecha_inicio, tiempo_practica, examenes, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                nombre,
                apellido,
                self.dni_input.text().strip(),
                self.cinturon_input.currentText(),
                self.fecha_inicio_input.text().strip(),
                int(self.tiempo_practica_input.text()) if self.tiempo_practica_input.text().isdigit() else 0,
                self.examenes_input.toPlainText(),
                self.observaciones_input.toPlainText()
            ))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Éxito", "Datos guardados correctamente")
        self.close()
