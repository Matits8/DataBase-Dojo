from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox
)
from PyQt6.QtCore import Qt


class AlumnoForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Alumno")
        self.setFixedSize(400, 400)
        self.parent = parent

        self.setStyleSheet("""
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #2e7d32;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.apellido_input = QLineEdit()
        self.nombre_input = QLineEdit()
        self.dni_input = QLineEdit()
        self.nac_input = QLineEdit()
        self.tel_input = QLineEdit()

        form_layout.addRow("Apellido:", self.apellido_input)
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("DNI:", self.dni_input)
        form_layout.addRow("Fecha de nacimiento:", self.nac_input)
        form_layout.addRow("Teléfono:", self.tel_input)

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar)

        layout.addLayout(form_layout)
        layout.addWidget(self.btn_guardar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def guardar(self):
        alumno = {
            "apellido": self.apellido_input.text(),
            "nombre": self.nombre_input.text(),
            "dni": self.dni_input.text(),
            "nac": self.nac_input.text(),
            "tel": self.tel_input.text(),
        }

        if self.parent:
            self.parent.agregar_alumno(alumno)
        self.close()
