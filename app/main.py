from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import sys
from app.alumno_form import AlumnoForm
from app.db import create_tables

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dojo Karate - Gestión de Alumnos")
        self.setMinimumSize(600, 400)

        # Ejemplo simple de contenido
        layout = QVBoxLayout()
        label = QLabel("¡Bienvenido al sistema de gestión del dojo!")
        layout.addWidget(label)

        # Definir el widget principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        
if __name__ == "__main__":
    create_tables()

    app = QApplication(sys.argv)
    form = AlumnoForm()         # para probar el formulario
    form.show()

    # window = MainWindow()        # para abrir la ventana principal
    # window.show()

    sys.exit(app.exec())