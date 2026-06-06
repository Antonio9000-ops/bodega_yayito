# prueba_logs.py (versión corregida)
import psycopg2
import logging
import os
from dotenv import load_dotenv

# =====================================================
# 1. CONFIGURACIÓN DE LOGGING
# =====================================================
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler("bodega_errores.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# =====================================================
# 2. CONEXIÓN A BD
# =====================================================
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:pass@localhost:5432/bodega_yayito")

def obtener_conexion():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logging.error(f"Error de conexión: {e}")
        return None

# =====================================================
# 3. FUNCIONES CRUD
# =====================================================
def registrar_producto(id_categoria, id_proveedor, id_unidad, nombre, sku,
                       stock_actual, stock_minimo, precio_venta, costo_promedio, fecha_vencimiento):
    query = """
    INSERT INTO productos (id_categoria, id_proveedor, id_unidad, nombre, sku,
                           stock_actual, stock_minimo, precio_venta, costo_promedio, fecha_vencimiento)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    conn = obtener_conexion()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(query, (id_categoria, id_proveedor, id_unidad, nombre, sku,
                            stock_actual, stock_minimo, precio_venta, costo_promedio, fecha_vencimiento))
        prod_id = cur.fetchone()[0]
        conn.commit()
        print(f"✅ Producto '{nombre}' registrado con ID {prod_id}")
        return prod_id
    except Exception as e:
        logging.error(f"Error registrando producto {nombre}: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

def registrar_movimiento(id_producto, tipo_movimiento, cantidad, costo_operacion, motivo):
    query = """
    INSERT INTO movimientos (id_producto, tipo_movimiento, cantidad, costo_operacion, motivo)
    VALUES (%s, %s, %s, %s, %s);
    """
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(query, (id_producto, tipo_movimiento.upper(), cantidad, costo_operacion, motivo))
        conn.commit()
        print(f"✅ Movimiento {tipo_movimiento} registrado para producto {id_producto}")
        return True
    except Exception as e:
        logging.error(f"Error registrando movimiento para producto {id_producto}: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def eliminar_producto(id_producto):
    query = "DELETE FROM productos WHERE id = %s;"
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(query, (id_producto,))
        conn.commit()
        print(f"✅ Producto {id_producto} eliminado.")
        return True
    except Exception as e:
        logging.error(f"Fallo al eliminar producto {id_producto}: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

# =====================================================
# 4. DATOS MAESTROS MÍNIMOS
# =====================================================
def poblar_datos_maestros():
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("INSERT INTO categorias (nombre) VALUES ('General') ON CONFLICT DO NOTHING RETURNING id;")
    cat = cur.fetchone()
    if not cat:
        cur.execute("SELECT id FROM categorias LIMIT 1;")
        cat_id = cur.fetchone()[0]
    else:
        cat_id = cat[0]

    cur.execute("INSERT INTO proveedores (nombre_empresa) VALUES ('Proveedor Test') ON CONFLICT DO NOTHING RETURNING id;")
    prov = cur.fetchone()
    if not prov:
        cur.execute("SELECT id FROM proveedores LIMIT 1;")
        prov_id = cur.fetchone()[0]
    else:
        prov_id = prov[0]

    cur.execute("INSERT INTO unidades_medida (nombre, abreviatura) VALUES ('Unidad', 'UND') ON CONFLICT DO NOTHING RETURNING id;")
    uni = cur.fetchone()
    if not uni:
        cur.execute("SELECT id FROM unidades_medida LIMIT 1;")
        uni_id = cur.fetchone()[0]
    else:
        uni_id = uni[0]

    conn.commit()
    cur.close()
    conn.close()
    return cat_id, prov_id, uni_id

# =====================================================
# 5. PRUEBA QUE GENERA EL ERROR DE FK (EL QUE SIRVE PARA LA DIAPOSITIVA)
# =====================================================
if __name__ == "__main__":
    print("=== GENERANDO ERROR DE VIOLACIÓN DE CLAVE FORÁNEA ===")

    cat_id, prov_id, uni_id = poblar_datos_maestros()

    # Crear producto con stock_actual = 0 (importante)
    prod_id = registrar_producto(cat_id, prov_id, uni_id,
                                 "ProductoConMovimientos", "FK999",
                                 0, 2, 15.0, 10.0, None)
    if not prod_id:
        exit()

    # Registrar entrada para que el Kardex tenga saldo positivo
    registrar_movimiento(prod_id, "ENTRADA", 10, 10.0, "Compra inicial")

    # Registrar una salida (esto crea un movimiento asociado)
    registrar_movimiento(prod_id, "SALIDA", 1, 10.0, "Venta de prueba")

    # Intentar eliminar el producto → aquí saltará el error de FK
    print("\n--- Intentando eliminar producto con movimientos asociados ---")
    exito = eliminar_producto(prod_id)

    if not exito:
        print("❌ Error esperado: No se pudo eliminar el producto. Revisa 'bodega_errores.log'")
    else:
        print("⚠️ Algo salió mal: el producto se eliminó a pesar de tener movimientos.")
