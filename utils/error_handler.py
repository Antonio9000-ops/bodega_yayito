import logging
import os

# Crear carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/sistema.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s'
)

class ErrorHandler:
    @staticmethod
    def log_error(error: Exception, modulo: str, funcion: str):
        mensaje = f"Módulo: {modulo} | Función: {funcion} | Error: {str(error)}"
        logging.error(mensaje)
        print("❌ Error registrado en logs/sistema.log")
