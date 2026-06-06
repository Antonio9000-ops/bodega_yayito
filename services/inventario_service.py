from models.producto_model import obtener_productos, registrar_producto as registrar_producto_db
from models.movimiento_model import registrar_movimiento
from services.producto_service import Producto
from services.movimiento_service import Movimiento
from utils.validators import detectar_productos_criticos

class BodegaController:
    def __init__(self):
        print("⚙️ BodegaController inicializado.")

    def registrar_producto_y_inventario(self, cat_id, prov_id, uni_id, nombre, sku,
                                         stock_init, stock_min, p_venta, costo, venci):
        # Crear producto en BD
        nuevo_id = registrar_producto_db(cat_id, prov_id, uni_id, nombre, sku,
                                         stock_init, stock_min, p_venta, costo, venci)
        if not nuevo_id:
            raise Exception("No se pudo registrar el producto")
        # Crear objeto Producto
        producto_obj = Producto(nuevo_id, nombre, sku, stock_init, stock_min,
                                p_venta, costo, cat_id, prov_id, uni_id, venci)
        # Si hay stock inicial, registrar movimiento de entrada
        if stock_init > 0:
            mov = Movimiento(producto_obj, "ENTRADA", stock_init, costo, "Inventario Inicial")
            mov.ejecutar()
        return producto_obj

    def realizar_movimiento(self, producto_id, tipo, cantidad, costo, motivo):
        # Obtener productos actuales desde BD
        lista_datos = obtener_productos()
        producto_obj = None
        for row in lista_datos:
            if row[0] == producto_id:
                producto_obj = Producto(row[0], row[1], row[2], row[3], row[4],
                                        row[5], row[6], row[7], row[8], row[9], row[10])
                break
        if not producto_obj:
            raise Exception(f"No se encontró producto con ID {producto_id}")
        mov = Movimiento(producto_obj, tipo, cantidad, costo, motivo)
        return mov.ejecutar()

    def obtener_inventario_actualizado(self):
        datos = obtener_productos()
        productos = []
        for row in datos:
            productos.append(Producto(row[0], row[1], row[2], row[3], row[4],
                                      row[5], row[6], row[7], row[8], row[9], row[10]))
        return productos

    def ver_estado_critico(self):
        productos = self.obtener_inventario_actualizado()
        criticos = detectar_productos_criticos(productos)
        print(f"\n🚨 TOTAL CRÍTICOS: {len(criticos)}")
        for p in criticos:
            print(p)
