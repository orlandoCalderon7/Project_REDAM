"""
Clase Consulta - Representa una búsqueda en el sistema
Responsabilidad: Almacenar criterios de búsqueda y generar códigos de validación
"""

from datetime import datetime
from utils.validaciones import Validaciones

class Consulta:
    """
    Clase boundary que maneja los datos de entrada del usuario
    """
    
    def __init__(self, tipo_consulta):
        """
        Constructor de Consulta
        
        Args:
            tipo_consulta (str): Tipo de búsqueda ('NOMBRES', 'DNI', 'FECHAS')
        """
        self.tipo_consulta = tipo_consulta
        self.apellido_paterno = ""
        self.apellido_materno = ""
        self.nombres = ""
        self.tipo_documento = ""
        self.numero_documento = ""
        self.fecha_inicial = None
        self.fecha_final = None
        self.codigo_validacion = None
        self.fecha_consulta = datetime.now()
    
    def consultar_por_nombres(self, apellido_paterno, apellido_materno="", nombres=""):
        """
        Configura consulta por nombres y apellidos
        
        Args:
            apellido_paterno (str): Apellido paterno (obligatorio)
            apellido_materno (str): Apellido materno (opcional)
            nombres (str): Nombres (obligatorio)
        
        Returns:
            bool: True si los datos son válidos
        """
        # Validar campos obligatorios
        if not apellido_paterno or not nombres:
            raise ValueError("Apellido paterno y nombres son obligatorios")
        
        # Validar formato
        if not Validaciones.validar_nombres(apellido_paterno):
            raise ValueError("Apellido paterno contiene caracteres inválidos")
        
        if apellido_materno and not Validaciones.validar_nombres(apellido_materno):
            raise ValueError("Apellido materno contiene caracteres inválidos")
        
        if not Validaciones.validar_nombres(nombres):
            raise ValueError("Nombres contienen caracteres inválidos")
        
        # Asignar valores
        self.apellido_paterno = apellido_paterno.strip().upper()
        self.apellido_materno = apellido_materno.strip().upper()
        self.nombres = nombres.strip().upper()
        self.tipo_consulta = "NOMBRES"
        
        return True
    
    def consultar_por_dni(self, tipo_documento, numero_documento):
        """
        Configura consulta por documento de identidad
        
        Args:
            tipo_documento (str): Tipo de documento (DNI, CE, PASAPORTE)
            numero_documento (str): Número del documento
        
        Returns:
            bool: True si los datos son válidos
        """
        # Validar campos obligatorios
        if not tipo_documento or not numero_documento:
            raise ValueError("Tipo y número de documento son obligatorios")
        
        # Validar según tipo de documento
        if tipo_documento == "DNI":
            if not Validaciones.validar_dni(numero_documento):
                raise ValueError("DNI debe tener 8 dígitos")
        elif tipo_documento == "CE":
            if not Validaciones.validar_carnet_extranjeria(numero_documento):
                raise ValueError("Carnet de extranjería debe tener 9 dígitos")
        elif tipo_documento == "PASAPORTE":
            if not Validaciones.validar_pasaporte(numero_documento):
                raise ValueError("Pasaporte debe tener entre 6 y 12 caracteres alfanuméricos")
        else:
            raise ValueError("Tipo de documento no válido")
        
        # Asignar valores
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento.strip().upper()
        self.tipo_consulta = "DNI"
        
        return True
    
    def consultar_por_fechas(self, fecha_inicial, fecha_final):
        """
        Configura consulta por rango de fechas
        
        Args:
            fecha_inicial (datetime): Fecha de inicio
            fecha_final (datetime): Fecha de fin
        
        Returns:
            bool: True si los datos son válidos
        """
        # Validar campos obligatorios
        if not fecha_inicial or not fecha_final:
            raise ValueError("Ambas fechas son obligatorias")
        
        # Validar que fecha inicial sea menor que fecha final
        if fecha_inicial > fecha_final:
            raise ValueError("La fecha inicial debe ser menor que la fecha final")
        
        # Validar que no sean fechas futuras
        if fecha_inicial > datetime.now() or fecha_final > datetime.now():
            raise ValueError("No se pueden consultar fechas futuras")
        
        # Validar rango máximo (ejemplo: 1 año)
        diferencia_dias = (fecha_final - fecha_inicial).days
        if diferencia_dias > 365:
            raise ValueError("El rango de fechas no puede superar 1 año")
        
        # Asignar valores
        self.fecha_inicial = fecha_inicial
        self.fecha_final = fecha_final
        self.tipo_consulta = "FECHAS"
        
        return True
    
    def ejecutar_consulta(self):
        """
        Prepara la consulta para ser ejecutada
        
        Returns:
            dict: Diccionario con los criterios de búsqueda
        """
        criterios = {
            'tipo': self.tipo_consulta,
            'fecha_consulta': self.fecha_consulta
        }
        
        if self.tipo_consulta == "NOMBRES":
            criterios['apellido_paterno'] = self.apellido_paterno
            criterios['apellido_materno'] = self.apellido_materno
            criterios['nombres'] = self.nombres
        
        elif self.tipo_consulta == "DNI":
            criterios['tipo_documento'] = self.tipo_documento
            criterios['numero_documento'] = self.numero_documento
        
        elif self.tipo_consulta == "FECHAS":
            criterios['fecha_inicial'] = self.fecha_inicial
            criterios['fecha_final'] = self.fecha_final
        
        return criterios
    
    def __str__(self):
        """Representación en string de la consulta"""
        return f"Consulta({self.tipo_consulta}) - {self.fecha_consulta.strftime('%d/%m/%Y %H:%M')}"
