import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QCheckBox,
    QListWidget, QListWidgetItem, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from reportlab.pdfgen import canvas
import openpyxl

class InformesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Informes de Alumnos")
        self.selected_fields = []
        self.selected_students = set()

        self.layout = QVBoxLayout()

        # Sección de selección de campos
        self.campo_label = QLabel("Seleccioná los campos a exportar:")
        self.layout.addWidget(self.campo_label)

        self.fields = ["nombre", "apellido", "dni", "fecha_nacimiento", "telefono", "email", "domicilio"]
        self.checkboxes = {}
        field_layout = QHBoxLayout()
        for field in self.fields:
            cb = QCheckBox(field.capitalize())
            self.checkboxes[field] = cb
            field_layout.addWidget(cb)
        self.layout.addLayout(field_layout)

        # Buscador
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar alumno por nombre o apellido")
        self.search_box.textChanged.connect(self.filter_alumnos)
        self.layout.addWidget(self.search_box)

        # Lista de alumnos con botones de selección
        self.lista_alumnos = QListWidget()
        self.layout.addWidget(self.lista_alumnos)

        # Botones exportar
        button_layout = QHBoxLayout()
        self.btn_pdf = QPushButton("Exportar a PDF")
        self.btn_pdf.clicked.connect(self.exportar_pdf)
        self.btn_excel = QPushButton("Exportar a Excel")
        self.btn_excel.clicked.connect(self.exportar_excel)
        button_layout.addWidget(self.btn_pdf)
        button_layout.addWidget(self.btn_excel)
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

        self.cargar_alumnos()

    def cargar_alumnos(self):
        self.lista_alumnos.clear()
        self.alumnos = []
        conn = sqlite3.connect("dojo.db")
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, apellido FROM alumnos")
        for id_, nombre, apellido in cur.fetchall():
            item = QListWidgetItem(f"{nombre} {apellido}")
            item.setData(Qt.ItemDataRole.UserRole, id_)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.lista_alumnos.addItem(item)
            self.alumnos.append((id_, nombre, apellido))
        conn.close()

    def filter_alumnos(self, texto):
        texto = texto.lower()
        self.lista_alumnos.clear()
        for id_, nombre, apellido in self.alumnos:
            if texto in nombre.lower() or texto in apellido.lower():
                item = QListWidgetItem(f"{nombre} {apellido}")
                item.setData(Qt.ItemDataRole.UserRole, id_)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.lista_alumnos.addItem(item)

    def obtener_seleccionados(self):
        campos = [f for f in self.fields if self.checkboxes[f].isChecked()]
        ids = []
        for i in range(self.lista_alumnos.count()):
            item = self.lista_alumnos.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                ids.append(item.data(Qt.ItemDataRole.UserRole))
        return campos, ids

    def exportar_pdf(self):
        campos, ids = self.obtener_seleccionados()
        if not campos or not ids:
            QMessageBox.warning(self, "Error", "Seleccioná al menos un campo y un alumno.")
            return

        conn = sqlite3.connect("dojo.db")
        cur = conn.cursor()

        c = canvas.Canvas("alumnos_exportados.pdf")
        y = 800
        for id_ in ids:
            cur.execute(f"SELECT {', '.join(campos)} FROM alumnos WHERE id = ?", (id_,))
            datos = cur.fetchone()
            linea = " | ".join(str(v) for v in datos)
            c.drawString(50, y, linea)
            y -= 20
            if y < 50:
                c.showPage()
                y = 800
        c.save()
        conn.close()
        QMessageBox.information(self, "Exportado", "PDF generado correctamente.")

    def exportar_excel(self):
        campos, ids = self.obtener_seleccionados()
        if not campos or not ids:
            QMessageBox.warning(self, "Error", "Seleccioná al menos un campo y un alumno.")
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append([c.capitalize() for c in campos])

        conn = sqlite3.connect("dojo.db")
        cur = conn.cursor()
        for id_ in ids:
            cur.execute(f"SELECT {', '.join(campos)} FROM alumnos WHERE id = ?", (id_,))
            datos = cur.fetchone()
            ws.append(datos)
        conn.close()

        wb.save("alumnos_exportados.xlsx")
        QMessageBox.information(self, "Exportado", "Excel generado correctamente.")
