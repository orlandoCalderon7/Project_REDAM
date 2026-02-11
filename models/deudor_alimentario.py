class DeudorAlimentario:
    def __init__(self, apellido_paterno, apellido_materno, nombres, 
                 tipo_documento, numero_documento, fecha_registro):
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.nombres = nombres
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.fecha_registro = fecha_registro
        self.foto = None
        self.expedientes = []
    
    def obtener_nombre_completo(self):
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombres}"
    
    def obtener_datos(self):
        return {
            'nombre_completo': self.obtener_nombre_completo(),
            'documento': f"{self.tipo_documento}: {self.numero_documento}",
            'fecha_registro': self.fecha_registro
        }
