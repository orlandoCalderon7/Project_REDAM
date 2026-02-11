"""
VentanaDetalle - Ventana modal que muestra información completa del deudor
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QGroupBox, QGridLayout, QScrollArea,
                             QWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class VentanaDetalle(QDialog):
    """
    Ventana modal para mostrar el detalle completo de un deudor
    """
    
    def __init__(self, deudor, parent=None):
        super().__init__(parent)
        self.deudor = deudor
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        self.setWindowTitle("Detalle del Deudor Alimentario Moroso")
        self.setGeometry(150, 150, 800, 600)
        self.setModal(True)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        titulo = QLabel("FICHA DETALLADA - DEUDOR ALIMENTARIO MOROSO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont('Arial', 16, QFont.Bold))
        titulo.setStyleSheet("""
            background-color: #8B0000;
            color: white;
            padding: 15px;
            border-radius: 5px;
        """)
        main_layout.addWidget(titulo)
        
        # Área con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)
        
        # Sección: Datos Personales
        grupo_personal = self._crear_grupo_datos_personales()
        content_layout.addWidget(grupo_personal)
        
        # Sección: Datos Judiciales (por cada expediente)
        if hasattr(self.deudor, 'expedientes') and self.deudor.expedientes:
            for i, expediente in enumerate(self.deudor.expedientes):
                grupo_judicial = self._crear_grupo_datos_judiciales(expediente, i+1)
                content_layout.addWidget(grupo_judicial)
        else:
            label_sin_exp = QLabel("⚠️ No hay expedientes disponibles")
            label_sin_exp.setStyleSheet("color: orange; font-size: 14px; padding: 20px;")
            content_layout.addWidget(label_sin_exp)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Botón Cerrar
        btn_cerrar = QPushButton("CERRAR")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 30px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
        """)
        btn_cerrar.clicked.connect(self.close)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cerrar)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)
        
        self.setLayout(main_layout)
    
    def _crear_grupo_datos_personales(self):
        """Crea el grupo de datos personales"""
        grupo = QGroupBox("DATOS PERSONALES DEL DEUDOR")
        grupo.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #8B0000;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # Foto (placeholder)
        label_foto = QLabel()
        label_foto.setFixedSize(120, 150)
        label_foto.setStyleSheet("""
            border: 2px solid #cccccc;
            background-color: #f0f0f0;
        """)
        label_foto.setAlignment(Qt.AlignCenter)
        label_foto.setText("FOTO\nNO\nDISPONIBLE")
        layout.addWidget(label_foto, 0, 0, 4, 1)
        
        # Datos
        row = 0
        self._agregar_campo(layout, row, 1, "Apellido Paterno:", 
                           self.deudor.apellido_paterno)
        row += 1
        self._agregar_campo(layout, row, 1, "Apellido Materno:", 
                           self.deudor.apellido_materno)
        row += 1
        self._agregar_campo(layout, row, 1, "Nombres:", 
                           self.deudor.nombres)
        row += 1
        self._agregar_campo(layout, row, 1, "Documento:", 
                           f"{self.deudor.tipo_documento}: {self.deudor.numero_documento}")
        row += 1
        self._agregar_campo(layout, row, 0, "Fecha de Registro:", 
                           self.deudor.fecha_registro, colspan=3)
        
        grupo.setLayout(layout)
        return grupo
    
    def _crear_grupo_datos_judiciales(self, expediente, numero):
        """Crea el grupo de datos judiciales"""
        grupo = QGroupBox(f"EXPEDIENTE N° {numero}")
        grupo.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(10)
        
        row = 0
        self._agregar_campo(layout, row, 0, "N° Expediente:", 
                           expediente.numero_expediente, colspan=2)
        row += 1
        self._agregar_campo(layout, row, 0, "Distrito Judicial:", 
                           expediente.distrito_judicial, colspan=2)
        row += 1
        self._agregar_campo(layout, row, 0, "Órgano Jurisdiccional:", 
                           expediente.organo_jurisdiccional, colspan=2)
        row += 1
        self._agregar_campo(layout, row, 0, "Secretario:", 
                           expediente.secretario, colspan=2)
        row += 1
        
        # Montos
        self._agregar_campo(layout, row, 0, "Pensión Mensual:", 
                           f"S/ {expediente.pension_mensual:.2f}")
        self._agregar_campo(layout, row, 1, "Importe Adeudado:", 
                           f"S/ {expediente.importe_adeudado:.2f}")
        row += 1
        self._agregar_campo(layout, row, 0, "Interés:", 
                           f"S/ {expediente.interes:.2f}")
        
        # Total
        total = expediente.calcular_monto_total()
        label_total = QLabel("TOTAL ADEUDADO:")
        label_total.setFont(QFont('Arial', 11, QFont.Bold))
        value_total = QLabel(f"S/ {total:.2f}")
        value_total.setFont(QFont('Arial', 11, QFont.Bold))
        value_total.setStyleSheet("color: #8B0000;")
        layout.addWidget(label_total, row, 1, Qt.AlignRight)
        layout.addWidget(value_total, row, 2)
        
        row += 1
        
        # Demandante
        if expediente.demandante:
            self._agregar_campo(layout, row, 0, "Demandante:", 
                               expediente.demandante.obtener_nombre_completo(), 
                               colspan=2)
            row += 1
            self._agregar_campo(layout, row, 0, "Relación:", 
                               expediente.demandante.relacion, colspan=2)
        
        grupo.setLayout(layout)
        return grupo
    
    def _agregar_campo(self, layout, row, col, etiqueta, valor, colspan=1):
        """Agrega un campo al layout"""
        label = QLabel(etiqueta)
        label.setFont(QFont('Arial', 10, QFont.Bold))
        label.setStyleSheet("color: #333;")
        
        value = QLabel(str(valor))
        value.setFont(QFont('Arial', 10))
        value.setStyleSheet("color: #000; background-color: #f9f9f9; padding: 5px; border-radius: 3px;")
        value.setWordWrap(True)
        
        layout.addWidget(label, row, col)
        layout.addWidget(value, row, col + 1, 1, colspan)
