"""
Servicio para conectar con la API real del REDAM
Responsabilidad: Realizar peticiones HTTP y parsear respuestas
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

class APIRedam:
    """
    Cliente para consumir la API del REDAM del Poder Judicial
    """
    
    BASE_URL = "https://casillas.pj.gob.pe/redam"
    TIMEOUT = 30  # segundos
    
    def __init__(self):
        """Inicializa sesión HTTP"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        self.view_state = None
        self.session_id = None
    
    def inicializar_sesion(self):
        """
        Inicializa la sesión obteniendo el ViewState de JSF
        
        Returns:
            bool: True si se inicializó correctamente
        """
        try:
            url = f"{self.BASE_URL}/services/consultaDeudor.xhtml"
            response = self.session.get(url, timeout=self.TIMEOUT)
            
            if response.status_code == 200:
                # Extraer ViewState (token de JSF)
                soup = BeautifulSoup(response.text, 'html.parser')
                view_state_input = soup.find('input', {'name': 'javax.faces.ViewState'})
                
                if view_state_input:
                    self.view_state = view_state_input.get('value')
                    return True
            
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"Error al inicializar sesión: {e}")
            return False
    
    def obtener_captcha_imagen(self):
        """
        Obtiene la imagen del captcha
        
        Returns:
            bytes: Imagen del captcha en formato bytes
        """
        try:
            url = f"{self.BASE_URL}/services/captcha.xhtml"
            response = self.session.get(url, timeout=self.TIMEOUT)
            
            if response.status_code == 200:
                return response.content
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f" Error al obtener captcha: {e}")
            return None
    
    def buscar_por_nombres(self, apellido_paterno, apellido_materno, nombres, captcha):
        """
        Busca deudores por nombres y apellidos
        
        Args:
            apellido_paterno (str): Apellido paterno
            apellido_materno (str): Apellido materno
            nombres (str): Nombres
            captcha (str): Código captcha
        
        Returns:
            list: Lista de diccionarios con datos de deudores
        """
        if not self.view_state:
            if not self.inicializar_sesion():
                raise Exception("No se pudo inicializar la sesión")
        
        try:
            url = f"{self.BASE_URL}/services/consultaDeudor.xhtml"
            
            # Datos del formulario
            data = {
                'formConsulta': 'formConsulta',
                'formConsulta:tipoConsulta': '1',  # 1 = Búsqueda por nombres
                'formConsulta:apellidoPaterno': apellido_paterno.upper(),
                'formConsulta:apellidoMaterno': apellido_materno.upper(),
                'formConsulta:nombres': nombres.upper(),
                'formConsulta:captcha': captcha.upper(),
                'formConsulta:btnConsultar': 'Consultar',
                'javax.faces.ViewState': self.view_state
            }
            
            # Realizar petición POST
            response = self.session.post(
                url, 
                data=data, 
                timeout=self.TIMEOUT,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return self._parsear_resultados(response.text)
            else:
                raise Exception(f"Error HTTP: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la petición: {str(e)}")
    
    def buscar_por_dni(self, tipo_documento, numero_documento, captcha):
        """
        Busca deudores por documento de identidad
        
        Args:
            tipo_documento (str): Tipo de documento
            numero_documento (str): Número de documento
            captcha (str): Código captcha
        
        Returns:
            list: Lista de diccionarios con datos de deudores
        """
        if not self.view_state:
            if not self.inicializar_sesion():
                raise Exception("No se pudo inicializar la sesión")
        
        try:
            url = f"{self.BASE_URL}/services/consultaDeudor.xhtml"
            
            # Mapear tipo de documento
            tipo_map = {
                'DNI': '1',
                'CARNET DE EXTRANJERÍA': '2',
                'PASAPORTE': '3'
            }
            
            data = {
                'formConsulta': 'formConsulta',
                'formConsulta:tipoConsulta': '2',  # 2 = Búsqueda por DNI
                'formConsulta:tipoDocumento': tipo_map.get(tipo_documento, '1'),
                'formConsulta:numeroDocumento': numero_documento,
                'formConsulta:captcha': captcha.upper(),
                'formConsulta:btnConsultar': 'Consultar',
                'javax.faces.ViewState': self.view_state
            }
            
            response = self.session.post(
                url, 
                data=data, 
                timeout=self.TIMEOUT,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return self._parsear_resultados(response.text)
            else:
                raise Exception(f"Error HTTP: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la petición: {str(e)}")
    
    def buscar_por_fechas(self, fecha_inicio, fecha_fin, captcha):
        """
        Busca deudores por rango de fechas
        
        Args:
            fecha_inicio (datetime): Fecha inicial
            fecha_fin (datetime): Fecha final
            captcha (str): Código captcha
        
        Returns:
            list: Lista de diccionarios con datos de deudores
        """
        if not self.view_state:
            if not self.inicializar_sesion():
                raise Exception("No se pudo inicializar la sesión")
        
        try:
            url = f"{self.BASE_URL}/services/consultaDeudor.xhtml"
            
            data = {
                'formConsulta': 'formConsulta',
                'formConsulta:tipoConsulta': '3',  # 3 = Búsqueda por fechas
                'formConsulta:fechaInicio': fecha_inicio.strftime('%d/%m/%Y'),
                'formConsulta:fechaFin': fecha_fin.strftime('%d/%m/%Y'),
                'formConsulta:captcha': captcha.upper(),
                'formConsulta:btnConsultar': 'Consultar',
                'javax.faces.ViewState': self.view_state
            }
            
            response = self.session.post(
                url, 
                data=data, 
                timeout=self.TIMEOUT,
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return self._parsear_resultados(response.text)
            else:
                raise Exception(f"Error HTTP: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la petición: {str(e)}")
    
    def obtener_detalle_deudor(self, id_deudor):
        """
        Obtiene el detalle completo de un deudor
        
        Args:
            id_deudor (str): ID del deudor en el sistema
        
        Returns:
            dict: Diccionario con información detallada
        """
        try:
            url = f"{self.BASE_URL}/services/detalleDeudor.xhtml"
            
            data = {
                'formDetalle': 'formDetalle',
                'formDetalle:idDeudor': id_deudor,
                'javax.faces.ViewState': self.view_state
            }
            
            response = self.session.post(
                url, 
                data=data, 
                timeout=self.TIMEOUT
            )
            
            if response.status_code == 200:
                return self._parsear_detalle(response.text)
            else:
                raise Exception(f"Error HTTP: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error en la petición: {str(e)}")
    
    def _parsear_resultados(self, html):
        """
        Parsea el HTML de respuesta y extrae los deudores
        
        Args:
            html (str): HTML de la respuesta
        
        Returns:
            list: Lista de diccionarios con datos de deudores
        """
        soup = BeautifulSoup(html, 'html.parser')
        deudores = []
        
        # Buscar tabla de resultados
        tabla = soup.find('table', {'id': re.compile(r'.*tablaResultados.*')})
        
        if not tabla:
            # No hay resultados
            return []
        
        # Extraer filas (ignorar header)
        filas = tabla.find_all('tr')[1:]  # Saltar header
        
        for fila in filas:
            celdas = fila.find_all('td')
            
            if len(celdas) >= 4:
                deudor = {
                    'nombre_completo': celdas[0].get_text(strip=True),
                    'tipo_documento': celdas[1].get_text(strip=True),
                    'numero_documento': celdas[2].get_text(strip=True),
                    'fecha_registro': celdas[3].get_text(strip=True),
                    'id': self._extraer_id_deudor(fila)
                }
                deudores.append(deudor)
        
        return deudores
    
    def _parsear_detalle(self, html):
        """
        Parsea el HTML del detalle del deudor
        
        Args:
            html (str): HTML de la respuesta
        
        Returns:
            dict: Diccionario con información detallada
        """
        soup = BeautifulSoup(html, 'html.parser')
        detalle = {}
        
        # Extraer datos personales
        detalle['apellido_paterno'] = self._extraer_campo(soup, 'apellidoPaterno')
        detalle['apellido_materno'] = self._extraer_campo(soup, 'apellidoMaterno')
        detalle['nombres'] = self._extraer_campo(soup, 'nombres')
        detalle['tipo_documento'] = self._extraer_campo(soup, 'tipoDocumento')
        detalle['numero_documento'] = self._extraer_campo(soup, 'numeroDocumento')
        
        # Extraer datos judiciales
        detalle['distrito_judicial'] = self._extraer_campo(soup, 'distritoJudicial')
        detalle['organo_jurisdiccional'] = self._extraer_campo(soup, 'organoJurisdiccional')
        detalle['secretario'] = self._extraer_campo(soup, 'secretario')
        detalle['numero_expediente'] = self._extraer_campo(soup, 'numeroExpediente')
        
        # Extraer montos
        detalle['pension_mensual'] = self._extraer_monto(soup, 'pensionMensual')
        detalle['importe_adeudado'] = self._extraer_monto(soup, 'importeAdeudado')
        detalle['interes'] = self._extraer_monto(soup, 'interes')
        
        # Extraer demandante
        detalle['demandante_nombre'] = self._extraer_campo(soup, 'demandanteNombre')
        detalle['demandante_relacion'] = self._extraer_campo(soup, 'demandanteRelacion')
        
        return detalle
    
    def _extraer_id_deudor(self, fila):
        """Extrae el ID del deudor desde el botón de detalle"""
        boton = fila.find('button') or fila.find('a')
        if boton:
            onclick = boton.get('onclick', '')
            match = re.search(r"'(\d+)'", onclick)
            if match:
                return match.group(1)
        return None
    
    def _extraer_campo(self, soup, id_campo):
        """Extrae un campo del HTML por su ID"""
        elemento = soup.find(id=re.compile(f'.*{id_campo}.*'))
        if elemento:
            return elemento.get_text(strip=True)
        return ""
    
    def _extraer_monto(self, soup, id_campo):
        """Extrae un monto y lo convierte a float"""
        texto = self._extraer_campo(soup, id_campo)
        # Limpiar formato: "S/ 1,500.00" -> 1500.00
        texto = texto.replace('S/', '').replace(',', '').strip()
        try:
            return float(texto)
        except ValueError:
            return 0.0
    
    def verificar_conexion(self):
        """
        Verifica si hay conexión con el servidor
        
        Returns:
            bool: True si hay conexión
        """
        try:
            response = self.session.get(
                self.BASE_URL, 
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
