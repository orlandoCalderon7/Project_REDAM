"""
TabFechas - Pestaña para búsqueda por rango de fechas
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QDateEdit, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from views.ventana_detalle import VentanaDetalle
from datetime import datetime

class TabFechas(QWidget):
    """
    Pestaña para consultar deudores por rango de fechas
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
        
        # Campo: Fecha Inicio
        fecha_inicio_layout = QHBoxLayout()
        label_inicio = QLabel("FECHA INICIO *")
        label_inicio.setFixedWidth(200)
        label_inicio.setFont(QFont('Arial', 10, QFont.Bold))
        
        self.date_inicio = QDateEdit()
        self.date_inicio.setCalendarPopup(True)
        self.date_inicio.setDate(QDate.currentDate().addMonths(-1))
        self.date_inicio.setDisplayFormat("dd/MM/yyyy")
        self.date_inicio.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QDateEdit:hover {
                border: 1px solid #8B0000;
            }
        """)
        
        fecha_inicio_layout.addWidget(label_inicio)
        fecha_inicio_layout.addWidget(self.date_inicio)
        layout.addLayout(fecha_inicio_layout)
        
        # Campo: Fecha Fin
        fecha_fin_layout = QHBoxLayout()
        label_fin = QLabel("FECHA FIN *")
        label_fin.setFixedWidth(200)
        label_fin.setFont(QFont('Arial', 10, QFont.Bold))
        
        self.date_fin = QDateEdit()
        self.date_fin.setCalendarPopup(True)
        self.date_fin.setDate(QDate.currentDate())
        self.date_fin.setDisplayFormat("dd/MM/yyyy")
        self.date_fin.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QDateEdit:hover {
                border: 1px solid #8B0000;
            }
        """)
        
        fecha_fin_layout.addWidget(label_fin)
        fecha_fin_layout.addWidget(self.date_fin)
        layout.addLayout(fecha_fin_layout)
        
        # Nota
        nota = QLabel("(*) El rango de periodos corresponde a la fecha en que se registro al deudor alimentario moroso.")
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
        
        label_captcha_texto = QLabel("Escriba el código mostrado")
        label_captcha_texto.setStyleSheet("font-size: 11px;")
        
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
        """Ejecuta la consulta por fechas"""
        try:
            captcha = self.input_captcha.text().strip()
            
            if not self.controlador.validar_captcha(captcha):
                QMessageBox.warning(self, "Validación", 
                    "El código captcha es incorrecto.")
                self.generar_captcha()
                return
            
            # Convertir QDate a datetime
            fecha_inicio = self.date_inicio.date().toPyDate()
            fecha_fin = self.date_fin.date().toPyDate()
            
            # Validar rango
            if fecha_inicio > fecha_fin:
                QMessageBox.warning(self, "Validación", 
                    "La fecha de inicio no puede ser mayor a la fecha fin.")
                return
            
            # Validar rango máximo (3 meses)
            dias_diferencia = (fecha_fin - fecha_inicio).days
            if dias_diferencia > 90:
                QMessageBox.warning(self, "Validación", 
                    "El rango máximo permitido es de 3 meses (90 días).")
                return
            
            self.setCursor(Qt.WaitCursor)
            
            try:
                # Convertir a datetime para la búsqueda
                fecha_inicio_dt = datetime.combine(fecha_inicio, datetime.min.time())
                fecha_fin_dt = datetime.combine(fecha_fin, datetime.max.time())
                
                resultados = self.controlador.buscar_por_fechas(
                    fecha_inicio_dt, fecha_fin_dt
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
                "No se encontraron registros en el rango de fechas especificado.")
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
            
            btn_detalle = QPushButton("🔍 Ver Detalle")
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
