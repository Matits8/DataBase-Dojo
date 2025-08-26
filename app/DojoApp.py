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

#from alumno_form2 import AlumnoForm  
from GUIs.menuPrincipal import MenuPrincipal
from core.dbManager import crear_base_datos

# Nombre de la base de datos
DB_NAME = "dojo.db"


class DojoApp():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MenuPrincipal()  

        #metodo de calse: db
        crear_base_datos()  # Se asegura de crear la DB al iniciar
        sys.exit(self.app.exec())
        
       
if __name__ == "__main__":
    # Crea una instancia de la clase Dojo para iniciar la aplicación
    dojo = DojoApp()
