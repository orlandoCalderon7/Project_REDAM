class Demandante:
    def __init__(self, apellido_paterno, apellido_materno, nombres, relacion):
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.nombres = nombres
        self.relacion = relacion
    
    def obtener_nombre_completo(self):
        return f"{self.apellido_paterno} {self.apellido_materno} {self.nombres}"
    
    def obtener_informacion(self):
        return {
            'nombre': self.obtener_nombre_completo(),
            'relacion': self.relacion
        }
