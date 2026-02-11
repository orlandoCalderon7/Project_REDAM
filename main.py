"""
Punto de entrada de la aplicación REDAM
Sistema de consulta de deudores alimentarios morosos
"""
import sys
from PyQt5.QtWidgets import QApplication
from views.ventana_principal import VentanaPrincipal

def main():
    """
    Función principal que inicia la aplicación
    """
    try:
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setStyle('Fusion')  # Estilo moderno multiplataforma
        
        # Crear ventana principal (sin parámetro por ahora)
        ventana = VentanaPrincipal()
        ventana.show()
        
        # Iniciar loop de eventos
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
