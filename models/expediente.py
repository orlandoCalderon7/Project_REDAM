class Expediente:
    def __init__(self, numero_expediente, distrito_judicial, 
                 organo_jurisdiccional, secretario, pension_mensual, 
                 importe_adeudado, interes):
        self.numero_expediente = numero_expediente
        self.distrito_judicial = distrito_judicial
        self.organo_jurisdiccional = organo_jurisdiccional
        self.secretario = secretario
        self.pension_mensual = pension_mensual
        self.importe_adeudado = importe_adeudado
        self.interes = interes
        self.demandante = None
    
    def calcular_monto_total(self):
        return self.importe_adeudado + self.interes
    
    def obtener_datos_judiciales(self):
        return {
            'expediente': self.numero_expediente,
            'distrito': self.distrito_judicial,
            'organo': self.organo_jurisdiccional,
            'secretario': self.secretario,
            'pension': f"S/ {self.pension_mensual:.2f}",
            'adeudado': f"S/ {self.importe_adeudado:.2f}",
            'interes': f"S/ {self.interes:.2f}",
            'total': f"S/ {self.calcular_monto_total():.2f}"
        }
