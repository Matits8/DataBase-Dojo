from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QListWidget, QListWidgetItem, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from db import obtener_todos_los_alumnos, buscar_alumnos

class InformesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.campos = ["nombre", "apellido", "dni", "fecha_nacimiento", "telefono", "email"]
        self.alumnos_seleccionados = set()

        self.init_ui()
        self.cargar_alumnos()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Sección de selección de campos
        campos_layout = QHBoxLayout()
        self.checkboxes = {}
        for campo in self.campos:
            cb = QCheckBox(campo.capitalize())
            cb.setChecked(True)
            self.checkboxes[campo] = cb
            campos_layout.addWidget(cb)
        layout.addLayout(campos_layout)

        # Buscador
        self.buscador = QLineEdit()
        self.buscador.setPlaceholderText("Buscar alumno por nombre o apellido...")
        self.buscador.textChanged.connect(self.buscar)
        layout.addWidget(self.buscador)

        # Lista de alumnos
        self.lista_alumnos = QListWidget()
        layout.addWidget(self.lista_alumnos)

        # Botones de exportación
        botones_layout = QHBoxLayout()
        self.btn_exportar_pdf = QPushButton("Exportar en PDF")
        self.btn_exportar_excel = QPushButton("Exportar en Excel")
        self.btn_exportar_pdf.clicked.connect(self.exportar_pdf)
        self.btn_exportar_excel.clicked.connect(self.exportar_excel)
        botones_layout.addWidget(self.btn_exportar_pdf)
        botones_layout.addWidget(self.btn_exportar_excel)
        layout.addLayout(botones_layout)

    def cargar_alumnos(self, filtro=""):
        self.lista_alumnos.clear()
        alumnos = buscar_alumnos(filtro) if filtro else obtener_todos_los_alumnos()
        for alumno in alumnos:
            item = QListWidgetItem(f"{alumno['nombre']} {alumno['apellido']}")
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setData(Qt.ItemDataRole.UserRole, alumno['id'])
            self.lista_alumnos.addItem(item)

    def buscar(self, texto):
        self.cargar_alumnos(filtro=texto)

    def obtener_campos_seleccionados(self):
        return [campo for campo, cb in self.checkboxes.items() if cb.isChecked()]

    def obtener_ids_seleccionados(self):
        ids = []
        for i in range(self.lista_alumnos.count()):
            item = self.lista_alumnos.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                ids.append(item.data(Qt.ItemDataRole.UserRole))
        return ids

    def exportar_pdf(self):
        campos = self.obtener_campos_seleccionados()
        ids = self.obtener_ids_seleccionados()
        QMessageBox.information(self, "Exportar PDF", f"Exportar PDF con campos: {campos}\nAlumnos: {ids}")
        # Aquí deberías llamar a una función que genere el PDF

    def exportar_excel(self):
        campos = self.obtener_campos_seleccionados()
        ids = self.obtener_ids_seleccionados()
        QMessageBox.information(self, "Exportar Excel", f"Exportar Excel con campos: {campos}\nAlumnos: {ids}")
        # Aquí deberías llamar a una función que genere el Excel
