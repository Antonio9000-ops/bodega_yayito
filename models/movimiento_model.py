from config.db_config import obtener_conexion

def registrar_movimiento(id_producto, tipo_movimiento, cantidad, costo_operacion, motivo):
    query = """
        INSERT INTO movimientos (id_producto, tipo_movimiento, cantidad, costo_operacion, motivo)
        VALUES (%s, %s, %s, %s, %s)
    """
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(query, (id_producto, tipo_movimiento, cantidad, costo_operacion, motivo))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
