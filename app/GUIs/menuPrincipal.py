from PyQt6 import uic
from PyQt6.QtWidgets import QMessageBox
import os

class MenuPrincipal:
    # Clase para manejar el menú principal de la aplicación
    # Esta clase carga la interfaz de usuario desde un archivo .ui 
    def __init__(self):
        #self.menu = uic.loadUi("resources/MenuPrincipal1.ui")
        ruta_ui = os.path.join(os.path.dirname(__file__), "..", "resources","ui", "MenuPrincipal1.ui")
        ruta_ui = os.path.abspath(ruta_ui)
        self.menu = uic.loadUi(ruta_ui)
        self.iniGUI()
        self.menu.show()
        

        

    # Método para inicializar la GUI y conectar botones
    def iniGUI(self):
        self.menu.But_AgrAlum.clicked.connect(self.abrir_formulario_alumno)
        self.menu.But_AgrGra.clicked.connect(self.no_implementado)
        self.menu.But_ModDat.clicked.connect(self.no_implementado)    
        self.menu.But_Asist.clicked.connect(self.no_implementado)
        self.menu.But_Exp.clicked.connect(self.no_implementado)
        self.menu.But_VerDat.clicked.connect(self.no_implementado)
        
        

    # Método para abrir el formulario de alumno
    # Este método se llama cuando se hace clic en el botón "Agregar Alumno"
    def abrir_formulario_alumno(self):
        from GUIs.alumFormAgre import alumFormAgre
        self.formulario_alumno = alumFormAgre(self.menu)
        self.menu.hide()
        
    
    
    def no_implementado(self):
        QMessageBox.information(self.menu, "Aviso", "Esta función aún no está implementada.")










"""
Extra tip: Si planeas mostrar más mensajes o interactuar con la interfaz, podrías considerar que tu clase MenuPrincipal herede de QMainWindow o QWidget, así podrías usar self directamente como widget.

Por ejemplo:
python
from PyQt6.QtWidgets import QMainWindow
class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("GUIs/MenuPrincipal1.ui", self)
        self.iniGUI()
        self.show()
"""