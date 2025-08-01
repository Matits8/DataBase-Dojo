from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,QTableWidget, QTableWidgetItem, QHBoxLayout
import sys
from app.alumno_form import AlumnoForm
from app.db import create_tables
from PyQt6.QtWidgets import QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dojo Karate - Gestión de Alumnos")
        self.setMinimumSize(800, 600)

        # Ejemplo simple de contenido
        layout = QVBoxLayout()
        label = QLabel("¡Bienvenido al sistema de gestión del dojo!")
        layout.addWidget(label)

        btn_alumnos = QPushButton("Gestión de Alumnos")
        btn_alumnos.clicked.connect(self.abrir_formulario_alumnos)
        layout.addWidget(btn_alumnos)

        # Definir el widget principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.cargar_alumnos_en_tabla()
        
        
    def abrir_formulario_alumnos(self):
        self.formulario = AlumnoForm()
        self.formulario.show()
    
    def cargar_alumnos_en_tabla(self):
        from app.db import obtener_todos_los_alumnos  # asegurate de tener esta función
        alumnos = obtener_todos_los_alumnos()
        
        self.tabla_alumnos.setRowCount(len(alumnos))
        for fila, alumno in enumerate(alumnos):
            self.tabla_alumnos.setItem(fila, 0, QTableWidgetItem(str(alumno[0])))  # id
            self.tabla_alumnos.setItem(fila, 1, QTableWidgetItem(alumno[1]))       # apellido
            self.tabla_alumnos.setItem(fila, 2, QTableWidgetItem(alumno[2]))       # nombre

            # Botón Editar
            btn_editar = QPushButton("Editar")
            btn_editar.clicked.connect(lambda _, id=alumno[0]: self.editar_alumno(id))
            self.tabla_alumnos.setCellWidget(fila, 3, btn_editar)

            # Botón Eliminar
            btn_eliminar = QPushButton("Eliminar")
            btn_eliminar.clicked.connect(lambda _, id=alumno[0]: self.eliminar_alumno(id))
            self.tabla_alumnos.setCellWidget(fila, 4, btn_eliminar)

    def editar_alumno(self, alumno_id):
        print(f"Editar alumno con ID: {alumno_id}")
        # Lógica de edición futura

    def eliminar_alumno(self, alumno_id):
        print(f"Eliminar alumno con ID: {alumno_id}")
        # Lógica de eliminación futura
    
        
if __name__ == "__main__":
    create_tables()

    app = QApplication(sys.argv)
    window = MainWindow()        # para abrir la ventana principal
    window.show()
    
    sys.exit(app.exec())