from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
import os

class alumFormAgre:
    # Clase para manejar el formulario de agregar alumno
    # Esta clase carga la interfaz de usuario desde un archivo .ui 
    def __init__(self, menu_principal):
        self.menu_principal = menu_principal
        ruta_ui = os.path.join(os.path.dirname(__file__), "..", "resources", "ui", "AgregarUi.ui")
        ruta_ui = os.path.abspath(ruta_ui)
        self.formulario = uic.loadUi(ruta_ui)
        self.iniGUI()
        self.formulario.show()

    # Método para inicializar la GUI y conectar botones
    def iniGUI(self):
        #Inicializa los campos del formulario
        #Botones de la GUI
        self.formulario.But_Exit.clicked.connect(self.volver_menu)
        self.formulario.toolButton.clicked.connect(self.VisibleCalendar1)
        self.formulario.toolButton_2.clicked.connect(self.VisibleCalendar2)
        
        
        #Invisible los campos que no se usan
        self.formulario.listViewSearch.setVisible(False)
        self.formulario.calendarWidget_2.setVisible(False)
        self.formulario.calendarWidget.setVisible(False)
        
        

    # Método para volver al menú principal
    def volver_menu(self):
        from GUIs.menuPrincipal import MenuPrincipal
        self.formulario.close()  # Cierra el formulario actual
        self.menu_principal.show()
        
    def VisibleCalendar1(self):
        # Método para mostrar el calendario
        self.formulario.calendarWidget.setVisible(True)
        self.formulario.calendarWidget_2.setVisible(False)
        self.formulario.listViewSearch.setVisible(False)
        
    def VisibleCalendar2(self):
        # Método para mostrar el calendario
        self.formulario.calendarWidget.setVisible(False)
        self.formulario.calendarWidget_2.setVisible(True)
        self.formulario.listViewSearch.setVisible(False)      
        
    def no_implementado(self):
        QMessageBox.information(self.menu, "Aviso", "Esta función aún no está implementada.")