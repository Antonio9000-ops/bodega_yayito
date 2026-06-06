import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

def obtener_conexion():
    try:
        DB_URL = os.getenv("DATABASE_URL")
        if not DB_URL:
            raise ValueError("No se encontró DATABASE_URL en el archivo .env")
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None
