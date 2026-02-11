"""
Clase Validaciones - Utilidades para validar datos de entrada
Responsabilidad: Validar formatos de datos según reglas de negocio
"""

import re
from datetime import datetime

class Validaciones:
    """
    Clase utilitaria con métodos estáticos para validación de datos
    """
    
    @staticmethod
    def validar_nombres(texto):
        """
        Valida que el texto contenga solo letras, espacios y tildes
        
        Args:
            texto (str): Texto a validar
        
        Returns:
            bool: True si es válido
        
        Ejemplos:
            >>> Validaciones.validar_nombres("JUAN CARLOS")
            True
            >>> Validaciones.validar_nombres("MARÍA JOSÉ")
            True
            >>> Validaciones.validar_nombres("JUAN123")
            False
        """
        if not texto or not texto.strip():
            return False
        
        # Patrón: solo letras (incluye tildes), espacios y guiones
        patron = r'^[A-ZÁÉÍÓÚÑa-záéíóúñ\s\-]+$'
        return bool(re.match(patron, texto.strip()))
    
    @staticmethod
    def validar_dni(dni):
        """
        Valida formato de DNI peruano (8 dígitos)
        
        Args:
            dni (str): DNI a validar
        
        Returns:
            bool: True si es válido
        
        Ejemplos:
            >>> Validaciones.validar_dni("12345678")
            True
            >>> Validaciones.validar_dni("1234567")
            False
            >>> Validaciones.validar_dni("1234567A")
            False
        """
        if not dni:
            return False
        
        # Eliminar espacios
        dni = dni.strip()
        
        # Debe tener exactamente 8 dígitos
        patron = r'^\d{8}$'
        return bool(re.match(patron, dni))
    
    @staticmethod
    def validar_carnet_extranjeria(carnet):
        """
        Valida formato de Carnet de Extranjería (9 dígitos)
        
        Args:
            carnet (str): Carnet a validar
        
        Returns:
            bool: True si es válido
        """
        if not carnet:
            return False
        
        carnet = carnet.strip()
        patron = r'^\d{9}$'
        return bool(re.match(patron, carnet))
    
    @staticmethod
    def validar_pasaporte(pasaporte):
        """
        Valida formato de pasaporte (6-12 caracteres alfanuméricos)
        
        Args:
            pasaporte (str): Pasaporte a validar
        
        Returns:
            bool: True si es válido
        """
        if not pasaporte:
            return False
        
        pasaporte = pasaporte.strip()
        
        # 6 a 12 caracteres alfanuméricos
        if len(pasaporte) < 6 or len(pasaporte) > 12:
            return False
        
        patron = r'^[A-Z0-9]+$'
        return bool(re.match(patron, pasaporte.upper()))
    
    @staticmethod
    def validar_fecha(fecha_str, formato="%d/%m/%Y"):
        """
        Valida y convierte una fecha en string a datetime
        
        Args:
            fecha_str (str): Fecha en formato string
            formato (str): Formato esperado (default: dd/mm/yyyy)
        
        Returns:
            datetime or None: Objeto datetime si es válido, None si no
        
        Ejemplos:
            >>> Validaciones.validar_fecha("15/03/2024")
            datetime.datetime(2024, 3, 15, 0, 0)
            >>> Validaciones.validar_fecha("32/13/2024")
            None
        """
        try:
            fecha = datetime.strptime(fecha_str, formato)
            return fecha
        except ValueError:
            return None
    
    @staticmethod
    def validar_rango_fechas(fecha_inicio, fecha_fin, max_dias=365):
        """
        Valida que un rango de fechas sea coherente
        
        Args:
            fecha_inicio (datetime): Fecha inicial
            fecha_fin (datetime): Fecha final
            max_dias (int): Máximo de días permitidos en el rango
        
        Returns:
            tuple: (bool, str) - (es_valido, mensaje_error)
        """
        # Verificar que ambas fechas existan
        if not fecha_inicio or not fecha_fin:
            return False, "Ambas fechas son obligatorias"
        
        # Verificar que fecha inicio sea menor que fecha fin
        if fecha_inicio > fecha_fin:
            return False, "La fecha inicial debe ser anterior a la fecha final"
        
        # Verificar que no sean fechas futuras
        hoy = datetime.now()
        if fecha_inicio > hoy:
            return False, "La fecha inicial no puede ser futura"
        if fecha_fin > hoy:
            return False, "La fecha final no puede ser futura"
        
        # Verificar rango máximo
        diferencia = (fecha_fin - fecha_inicio).days
        if diferencia > max_dias:
            return False, f"El rango no puede superar {max_dias} días"
        
        return True, "Rango válido"
    
    @staticmethod
    def validar_captcha(codigo_ingresado, codigo_esperado):
        """
        Valida que el código captcha ingresado sea correcto
        
        Args:
            codigo_ingresado (str): Código ingresado por el usuario
            codigo_esperado (str): Código generado por el sistema
        
        Returns:
            bool: True si coinciden (case-insensitive)
        """
        if not codigo_ingresado or not codigo_esperado:
            return False
        
        return codigo_ingresado.strip().upper() == codigo_esperado.strip().upper()
    
    @staticmethod
    def limpiar_texto(texto):
        """
        Limpia un texto eliminando espacios extras y caracteres especiales
        
        Args:
            texto (str): Texto a limpiar
        
        Returns:
            str: Texto limpio
        """
        if not texto:
            return ""
        
        # Eliminar espacios al inicio y final
        texto = texto.strip()
        
        # Reemplazar múltiples espacios por uno solo
        texto = re.sub(r'\s+', ' ', texto)
        
        return texto
    
    @staticmethod
    def validar_monto(monto):
        """
        Valida que un monto sea un número positivo
        
        Args:
            monto (float): Monto a validar
        
        Returns:
            bool: True si es válido
        """
        try:
            monto_float = float(monto)
            return monto_float >= 0
        except (ValueError, TypeError):
            return False
