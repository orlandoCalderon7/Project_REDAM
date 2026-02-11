"""
TabDNI - Pestaña para búsqueda por documento de identidad
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from views.ventana_detalle import VentanaDetalle

class TabDNI(QWidget):
    """
    Pestaña para consultar deudores por documento de identidad
    """
    
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Campo: Tipo de Documento
        tipo_layout = QHBoxLayout()
        label_tipo = QLabel("TIPO DE DOCUMENTO *")
        label_tipo.setFixedWidth(200)
        label_tipo.setFont(QFont('Arial', 10, QFont.Bold))
        
        self.combo_tipo_documento = QComboBox()
        self.combo_tipo_documento.addItems([
            "Seleccione",
            "DNI",
            "CARNET DE EXTRANJERÍA",
            "PASAPORTE"
        ])
        self.combo_tipo_documento.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QComboBox:hover {
                border: 1px solid #8B0000;
            }
        """)
        
        tipo_layout.addWidget(label_tipo)
        tipo_layout.addWidget(self.combo_tipo_documento)
        layout.addLayout(tipo_layout)
        
        # Campo: Número de Documento
        numero_layout = QHBoxLayout()
        label_numero = QLabel("NÚMERO DE DOCUMENTO *")
        label_numero.setFixedWidth(200)
        label_numero.setFont(QFont('Arial', 10, QFont.Bold))
        
        self.input_numero_documento = QLineEdit()
        self.input_numero_documento.setPlaceholderText("Número de Documento")
        self.input_numero_documento.setMaxLength(12)
        self.input_numero_documento.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QLineEdit:focus {
                border: 2px solid #8B0000;
            }
        """)
        
        numero_layout.addWidget(label_numero)
        numero_layout.addWidget(self.input_numero_documento)
        layout.addLayout(numero_layout)
        
        # Nota
        nota = QLabel("(*) Datos obligatorios.")
        nota.setStyleSheet("color: red; font-size: 11px;")
        layout.addWidget(nota)
        
        # CAPTCHA
        captcha_layout = QHBoxLayout()
        
        self.label_captcha = QLabel()
        self.label_captcha.setStyleSheet("""
            background-color: #8B0000;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            letter-spacing: 5px;
        """)
        self.label_captcha.setFixedHeight(50)
        
        btn_refresh = QPushButton("🔄")
        btn_refresh.setFixedSize(50, 50)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        btn_refresh.clicked.connect(self.generar_captcha)
        
        self.input_captcha = QLineEdit()
        self.input_captcha.setPlaceholderText("Código")
        self.input_captcha.setMaxLength(4)
        self.input_captcha.setFixedWidth(150)
        self.input_captcha.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)
        
        # Generar captcha después de crear los widgets
        self.generar_captcha()
        
        captcha_layout.addStretch()
        captcha_layout.addWidget(self.label_captcha)
        captcha_layout.addWidget(btn_refresh)
        captcha_layout.addWidget(self.input_captcha)
        captcha_layout.addStretch()
        
        layout.addLayout(captcha_layout)
        
        # Botón Consultar
        btn_consultar = QPushButton("CONSULTAR")
        btn_consultar.setStyleSheet("""
            QPushButton {
                background-color: #8B0000;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 40px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #A52A2A;
            }
        """)
        btn_consultar.clicked.connect(self.realizar_consulta)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_consultar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Tabla de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(5)
        self.tabla_resultados.setHorizontalHeaderLabels([
            "Apellidos y Nombres", "Tipo Doc.", "N° Documento", 
            "Fecha Registro", "Detalle"
        ])
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_resultados.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #8B0000;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
        """)
        self.tabla_resultados.setVisible(False)
        layout.addWidget(self.tabla_resultados)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def generar_captcha(self):
        """Genera y muestra un nuevo código captcha"""
        codigo = self.controlador.generar_captcha()
        self.label_captcha.setText(codigo)
        self.input_captcha.clear()
        self.input_captcha.setFocus()
    
    def realizar_consulta(self):
        """Ejecuta la consulta por DNI"""
        try:
            tipo_documento = self.combo_tipo_documento.currentText()
            numero_documento = self.input_numero_documento.text().strip()
            captcha = self.input_captcha.text().strip()
            
            if tipo_documento == "Seleccione":
                QMessageBox.warning(self, "Validación", 
                    "Debe seleccionar un tipo de documento.")
                return
            
            if not numero_documento:
                QMessageBox.warning(self, "Validación", 
                    "Debe ingresar el número de documento.")
                return
            
            if not self.controlador.validar_captcha(captcha):
                QMessageBox.warning(self, "Validación", 
                    "El código captcha es incorrecto.")
                self.generar_captcha()
                return
            
            self.setCursor(Qt.WaitCursor)
            
            try:
                resultados = self.controlador.buscar_por_dni(
                    tipo_documento, numero_documento
                )
                self.mostrar_resultados(resultados)
            finally:
                self.setCursor(Qt.ArrowCursor)
                
        except Exception as e:
            self.setCursor(Qt.ArrowCursor)
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
            self.generar_captcha()
    
    def mostrar_resultados(self, deudores):
        """Muestra los resultados en la tabla"""
        if not deudores:
            QMessageBox.information(self, "Sin resultados",
                "Los datos ingresados no presentan registros.")
            self.tabla_resultados.setVisible(False)
            return
        
        self.tabla_resultados.setRowCount(len(deudores))
        
        for i, deudor in enumerate(deudores):
            self.tabla_resultados.setItem(i, 0, 
                QTableWidgetItem(deudor.obtener_nombre_completo()))
            self.tabla_resultados.setItem(i, 1, 
                QTableWidgetItem(deudor.tipo_documento))
            self.tabla_resultados.setItem(i, 2, 
                QTableWidgetItem(deudor.numero_documento))
            self.tabla_resultados.setItem(i, 3, 
                QTableWidgetItem(deudor.fecha_registro))
            
            btn_detalle = QPushButton("Ver Detalle")
            btn_detalle.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            btn_detalle.clicked.connect(
                lambda checked, d=deudor: self.ver_detalle(d)
            )
            self.tabla_resultados.setCellWidget(i, 4, btn_detalle)
        
        self.tabla_resultados.setVisible(True)
    
    def ver_detalle(self, deudor):
        """Abre ventana de detalle"""
        try:
            ventana_detalle = VentanaDetalle(deudor, self)
            ventana_detalle.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
