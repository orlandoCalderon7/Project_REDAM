"""
VentanaPrincipal - Ventana principal de la aplicación
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QTabWidget,
                             QLabel, QMessageBox, QStatusBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Importaciones locales
from controllers.controlador_redam import ControladorREDAM
from views.tab_nombres import TabNombres
from views.tab_dni import TabDNI
from views.tab_fechas import TabFechas

class VentanaPrincipal(QMainWindow):
    """
    Ventana principal del sistema REDAM
    """
    
    def __init__(self):
        """Constructor de la ventana principal"""
        super().__init__()
        
        # Inicializar controlador (sin parámetros por ahora)
        try:
            self.controlador = ControladorREDAM()
            print("Controlador inicializado correctamente")
        except Exception as e:
            print(f" Error al inicializar controlador: {e}")
            import traceback
            traceback.print_exc()
        
        # Inicializar interfaz
        self.init_ui()
        
        # Mostrar estado
        self.mostrar_estado_conexion()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle('Sistema REDAM - Poder Judicial del Perú')
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Título
        titulo = QLabel('Deudores Alimentarios Morosos - DAM')
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont('Arial', 18, QFont.Bold))
        titulo.setStyleSheet("""
            color: #8B0000;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
        """)
        layout.addWidget(titulo)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #cccccc;
                background: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background: #f0f0f0;
                color: #333;
                padding: 12px 25px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #8B0000;
                color: white;
            }
            QTabBar::tab:hover {
                background: #A52A2A;
                color: white;
            }
        """)
        
        # Crear pestañas
        try:
            self.tab_nombres = TabNombres(self.controlador)
            self.tab_dni = TabDNI(self.controlador)
            self.tab_fechas = TabFechas(self.controlador)
            
            self.tabs.addTab(self.tab_nombres, " NOMBRES Y APELLIDOS")
            self.tabs.addTab(self.tab_dni, " DOCUMENTO DE IDENTIDAD")
            self.tabs.addTab(self.tab_fechas, "RANGO DE PERIODOS")
            
            print(" Pestañas creadas correctamente")
            
        except Exception as e:
            print(f" Error al crear pestañas: {e}")
            import traceback
            traceback.print_exc()
        
        layout.addWidget(self.tabs)
        
        # Barra de estado
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #f0f0f0;
                border-top: 2px solid #cccccc;
                padding: 5px;
            }
        """)
    
    def mostrar_estado_conexion(self):
        """Muestra el estado de conexión en la barra de estado"""
        if hasattr(self.controlador, 'usar_api') and self.controlador.usar_api:
            mensaje = " Conectado a API real del REDAM"
            color = "green"
        else:
            mensaje = " "
            color = "orange"
        
        self.status_bar.showMessage(mensaje)
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: #f0f0f0;
                border-top: 2px solid #cccccc;
                padding: 5px;
                color: {color};
                font-weight: bold;
            }}
        """)
