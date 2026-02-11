"""
Controlador REDAM - Gestiona la lógica de negocio
"""

import random
import string
import json
import os
from datetime import datetime
from models.deudor_alimentario import DeudorAlimentario
from models.expediente import Expediente
from models.demandante import Demandante

class ControladorREDAM:
    """
    Controlador principal del sistema REDAM
    """
    
    def __init__(self, usar_api_real=False):
        """
        Constructor
        
        Args:
            usar_api_real (bool): Si True, intenta usar API real (no implementado aún)
        """
        self.usar_api = False  # Por ahora siempre False
        self.captcha_actual = None
        self.deudores_bd = self._cargar_datos_desde_json()
        
        print(f"✅ Controlador inicializado con {len(self.deudores_bd)} deudores")
    
    def _cargar_datos_desde_json(self):
        """
        Carga deudores desde archivo JSON
        
        Returns:
            list: Lista de objetos DeudorAlimentario
        """
        try:
            # Obtener ruta del archivo JSON
            ruta_actual = os.path.dirname(__file__)
            ruta_json = os.path.join(ruta_actual, '..', 'data', 'deudores_mock.json')
            
            # Verificar si existe
            if not os.path.exists(ruta_json):
                print(f"⚠️ Archivo no encontrado: {ruta_json}")
                return self._crear_datos_mock()
            
            # Leer archivo
            with open(ruta_json, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            # Convertir JSON a objetos
            deudores = []
            for d in datos['deudores']:
                # Crear deudor
                deudor = DeudorAlimentario(
                    d['apellido_paterno'],
                    d['apellido_materno'],
                    d['nombres'],
                    d['tipo_documento'],
                    d['numero_documento'],
                    d['fecha_registro']
                )
                
                # Agregar expedientes
                for e in d['expedientes']:
                    expediente = Expediente(
                        e['numero_expediente'],
                        e['distrito_judicial'],
                        e['organo_jurisdiccional'],
                        e['secretario'],
                        e['pension_mensual'],
                        e['importe_adeudado'],
                        e['interes']
                    )
                    
                    # Agregar demandante
                    dem = e['demandante']
                    demandante = Demandante(
                        dem['apellido_paterno'],
                        dem['apellido_materno'],
                        dem['nombres'],
                        dem['relacion']
                    )
                    
                    expediente.demandante = demandante
                    deudor.expedientes.append(expediente)
                
                deudores.append(deudor)
            
            print(f"✅ Cargados {len(deudores)} deudores desde JSON")
            return deudores
            
        except FileNotFoundError:
            print("⚠️ Archivo deudores_mock.json no encontrado")
            return self._crear_datos_mock()
        except json.JSONDecodeError as e:
            print(f"⚠️ Error al leer JSON: {e}")
            return self._crear_datos_mock()
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return self._crear_datos_mock()
    
    def _crear_datos_mock(self):
        """
        Crea datos de prueba en memoria si no hay JSON
        
        Returns:
            list: Lista de objetos DeudorAlimentario
        """
        print("🔄 Creando datos mock en memoria...")
        
        deudores = []
        
        # Deudor 1
        deudor1 = DeudorAlimentario(
            "GARCIA", "LOPEZ", "JUAN CARLOS",
            "DNI", "12345678", "15/03/2024"
        )
        
        expediente1 = Expediente(
            "00123-2024-0-1801-JP-FC-01",
            "LIMA",
            "1° JUZGADO DE PAZ LETRADO DE SAN JUAN DE LURIGANCHO",
            "DR. MARTINEZ SILVA ROBERTO",
            1500.00, 4500.00, 450.00
        )
        
        demandante1 = Demandante(
            "RODRIGUEZ", "PEREZ", "MARIA ELENA", "MADRE"
        )
        
        expediente1.demandante = demandante1
        deudor1.expedientes.append(expediente1)
        deudores.append(deudor1)
        
        # Deudor 2
        deudor2 = DeudorAlimentario(
            "FERNANDEZ", "TORRES", "PEDRO ANTONIO",
            "DNI", "87654321", "20/02/2024"
        )
        
        expediente2 = Expediente(
            "00456-2024-0-1801-JP-FC-02",
            "LIMA",
            "2° JUZGADO DE PAZ LETRADO DE ATE",
            "DRA. GOMEZ RAMIREZ ANA",
            2000.00, 8000.00, 800.00
        )
        
        demandante2 = Demandante(
            "CASTRO", "DIAZ", "CARMEN ROSA", "MADRE"
        )
        
        expediente2.demandante = demandante2
        deudor2.expedientes.append(expediente2)
        deudores.append(deudor2)
        
        print(f"✅ Creados {len(deudores)} deudores mock")
        return deudores
    
    def generar_captcha(self):
        """
        Genera código captcha aleatorio
        
        Returns:
            str: Código de 4 caracteres
        """
        self.captcha_actual = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=4)
        )
        return self.captcha_actual
    
    def validar_captcha(self, codigo_ingresado):
        """
        Valida el código captcha
        
        Args:
            codigo_ingresado (str): Código ingresado por el usuario
        
        Returns:
            bool: True si es correcto
        """
        if not codigo_ingresado or not self.captcha_actual:
            return False
        
        return codigo_ingresado.strip().upper() == self.captcha_actual.upper()
    
    def buscar_por_nombres(self, apellido_paterno, apellido_materno="", nombres=""):
        """
        Busca deudores por nombres y apellidos
        
        Args:
            apellido_paterno (str): Apellido paterno
            apellido_materno (str): Apellido materno (opcional)
            nombres (str): Nombres
        
        Returns:
            list: Lista de DeudorAlimentario encontrados
        """
        resultados = []
        
        for deudor in self.deudores_bd:
            # Comparación case-insensitive
            coincide_paterno = apellido_paterno.upper() in deudor.apellido_paterno.upper()
            
            coincide_materno = (
                not apellido_materno or 
                apellido_materno.upper() in deudor.apellido_materno.upper()
            )
            
            coincide_nombres = (
                not nombres or 
                nombres.upper() in deudor.nombres.upper()
            )
            
            if coincide_paterno and coincide_materno and coincide_nombres:
                resultados.append(deudor)
        
        return resultados
    
    def buscar_por_dni(self, tipo_documento, numero_documento):
        """
        Busca deudores por documento de identidad
        
        Args:
            tipo_documento (str): Tipo de documento
            numero_documento (str): Número de documento
        
        Returns:
            list: Lista de DeudorAlimentario encontrados
        """
        for deudor in self.deudores_bd:
            if (deudor.tipo_documento == tipo_documento and 
                deudor.numero_documento == numero_documento):
                return [deudor]
        
        return []
    
    def buscar_por_fechas(self, fecha_inicio, fecha_fin):
        """
        Busca deudores por rango de fechas de registro
        
        Args:
            fecha_inicio (datetime): Fecha inicial
            fecha_fin (datetime): Fecha final
        
        Returns:
            list: Lista de DeudorAlimentario encontrados
        """
        resultados = []
        
        for deudor in self.deudores_bd:
            try:
                # Convertir fecha de registro a datetime
                fecha_registro = datetime.strptime(deudor.fecha_registro, '%d/%m/%Y')
                
                # Verificar si está en el rango
                if fecha_inicio <= fecha_registro <= fecha_fin:
                    resultados.append(deudor)
            except ValueError:
                # Si la fecha no se puede parsear, ignorar
                continue
        
        return resultados
    
    def obtener_expediente_completo(self, deudor, index_expediente=0):
        """
        Obtiene el expediente completo de un deudor
        
        Args:
            deudor (DeudorAlimentario): Deudor
            index_expediente (int): Índice del expediente
        
        Returns:
            Expediente: Expediente completo o None
        """
        if index_expediente < len(deudor.expedientes):
            return deudor.expedientes[index_expediente]
        return None
