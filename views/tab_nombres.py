"""
TabNombres - Pestaña para búsqueda por nombres y apellidos
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from views.ventana_detalle import VentanaDetalle

class TabNombres(QWidget):
    """
    Pestaña para consultar deudores por nombres y apellidos
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
        
        # Campo: Apellido Paterno
        self.input_apellido_paterno = self._crear_campo("APELLIDO PATERNO *", layout)
        
        # Campo: Apellido Materno
        self.input_apellido_materno = self._crear_campo("APELLIDO MATERNO", layout)
        
        # Campo: Nombres
        self.input_nombres = self._crear_campo("NOMBRES *", layout)
        
        # Nota de campos obligatorios
        nota = QLabel("* Para realizar la búsqueda se requiere como mínimo un APELLIDO PATERNO y un NOMBRE.")
        nota.setStyleSheet("color: red; font-size: 11px;")
        nota.setWordWrap(True)
        layout.addWidget(nota)
        
        # Sección CAPTCHA
        captcha_layout = QHBoxLayout()
        
        # Label del captcha
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
        
        # Botón refresh
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
        
        # Label de texto
        label_captcha_texto = QLabel("Escriba el código mostrado")
        label_captcha_texto.setStyleSheet("font-size: 11px;")
        
        # Input del captcha - CREAR ANTES DE LLAMAR generar_captcha()
        self.input_captcha = QLineEdit()
        self.input_captcha.setPlaceholderText("Código")
        self.input_captcha.setMaxLength(4)
        self.input_captcha.setFixedWidth(150)
        self.input_captcha.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                text-transform: uppercase;
            }
        """)
        
        # AHORA SÍ generar el captcha (después de crear input_captcha)
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
            QPushButton:pressed {
                background-color: #6B0000;
            }
        """)
        btn_consultar.clicked.connect(self.realizar_consulta)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_consultar)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Tabla de resultados (inicialmente oculta)
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
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #8B0000;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
        """)
        self.tabla_resultados.setVisible(False)
        layout.addWidget(self.tabla_resultados)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _crear_campo(self, etiqueta, layout):
        """
        Crea un campo de entrada con su etiqueta
        
        Args:
            etiqueta (str): Texto de la etiqueta
            layout (QVBoxLayout): Layout donde agregar el campo
        
        Returns:
            QLineEdit: Campo de entrada creado
        """
        campo_layout = QHBoxLayout()
        
        label = QLabel(etiqueta)
        label.setFixedWidth(200)
        label.setFont(QFont('Arial', 10, QFont.Bold))
        
        input_field = QLineEdit()
        input_field.setPlaceholderText(etiqueta.replace('*', '').strip().title())
        input_field.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QLineEdit:focus {
                border: 2px solid #8B0000;
            }
        """)
        
        campo_layout.addWidget(label)
        campo_layout.addWidget(input_field)
        
        layout.addLayout(campo_layout)
        return input_field
    
    def generar_captcha(self):
        """Genera y muestra un nuevo código captcha"""
        codigo = self.controlador.generar_captcha()
        self.label_captcha.setText(codigo)
        self.input_captcha.clear()
        self.input_captcha.setFocus()
    
    def realizar_consulta(self):
        """
        Ejecuta la consulta por nombres
        Valida los datos y muestra resultados
        """
        try:
            # Obtener valores de los campos
            apellido_paterno = self.input_apellido_paterno.text().strip()
            apellido_materno = self.input_apellido_materno.text().strip()
            nombres = self.input_nombres.text().strip()
            captcha = self.input_captcha.text().strip()
            
            # Validar campos obligatorios
            if not apellido_paterno or not nombres:
                QMessageBox.warning(self, "Validación", 
                    "Debe ingresar al menos un APELLIDO PATERNO y un NOMBRE.")
                self.input_apellido_paterno.setFocus()
                return
            
            # Validar captcha
            if not self.controlador.validar_captcha(captcha):
                QMessageBox.warning(self, "Validación", 
                    "El código captcha es incorrecto.")
                self.generar_captcha()
                return
            
            # Mostrar cursor de espera
            self.setCursor(Qt.WaitCursor)
            
            try:
                # Realizar búsqueda
                resultados = self.controlador.buscar_por_nombres(
                    apellido_paterno, apellido_materno, nombres
                )
                
                # Mostrar resultados
                self.mostrar_resultados(resultados)
                
            finally:
                # Restaurar cursor normal
                self.setCursor(Qt.ArrowCursor)
            
        except Exception as e:
            self.setCursor(Qt.ArrowCursor)
            QMessageBox.critical(self, "Error", 
                f"Ocurrió un error al realizar la consulta:\n{str(e)}")
            self.generar_captcha()
    
    def mostrar_resultados(self, deudores):
        """
        Muestra los deudores encontrados en la tabla
        
        Args:
            deudores (list): Lista de objetos DeudorAlimentario
        """
        if not deudores:
            QMessageBox.information(self, "Sin resultados",
                "Los datos ingresados no presentan registros.")
            self.tabla_resultados.setVisible(False)
            return
        
        # Configurar número de filas
        self.tabla_resultados.setRowCount(len(deudores))
        
        # Llenar tabla
        for i, deudor in enumerate(deudores):
            # Columna 0: Nombre completo
            self.tabla_resultados.setItem(i, 0, 
                QTableWidgetItem(deudor.obtener_nombre_completo()))
            
            # Columna 1: Tipo de documento
            self.tabla_resultados.setItem(i, 1, 
                QTableWidgetItem(deudor.tipo_documento))
            
            # Columna 2: Número de documento
            self.tabla_resultados.setItem(i, 2, 
                QTableWidgetItem(deudor.numero_documento))
            
            # Columna 3: Fecha de registro
            self.tabla_resultados.setItem(i, 3, 
                QTableWidgetItem(deudor.fecha_registro))
            
            # Columna 4: Botón de detalle
            btn_detalle = QPushButton(" Ver Detalle")
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
            # Usar lambda para capturar el deudor actual
            btn_detalle.clicked.connect(
                lambda checked, d=deudor: self.ver_detalle(d)
            )
            self.tabla_resultados.setCellWidget(i, 4, btn_detalle)
        
        # Mostrar tabla
        self.tabla_resultados.setVisible(True)
    
    def ver_detalle(self, deudor):
        """
        Abre ventana con el detalle completo del deudor
        
        Args:
            deudor (DeudorAlimentario): Deudor seleccionado
        """
        try:
            ventana_detalle = VentanaDetalle(deudor, self)
            ventana_detalle.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                f"Error al abrir detalle:\n{str(e)}")
