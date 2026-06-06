from config.db_config import obtener_conexion

def registrar_producto(id_categoria, id_proveedor, id_unidad, nombre, sku,
                       stock_actual, stock_minimo, precio_venta, costo_promedio,
                       fecha_vencimiento=None):
    query = """
        INSERT INTO productos (id_categoria, id_proveedor, id_unidad, nombre,
                               sku, stock_actual, stock_minimo, precio_venta,
                               costo_promedio, fecha_vencimiento)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """
    conn = obtener_conexion()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(query, (id_categoria, id_proveedor, id_unidad, nombre, sku,
                            stock_actual, stock_minimo, precio_venta,
                            costo_promedio, fecha_vencimiento))
        producto_id = cur.fetchone()[0]
        conn.commit()
        return producto_id
    except Exception as e:
        conn.rollback()
        print(f"❌ Error al registrar producto: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def obtener_productos():
    query = "SELECT id, nombre, sku, stock_actual, stock_minimo, precio_venta, costo_promedio, id_categoria, id_proveedor, id_unidad, fecha_vencimiento FROM productos"
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()
