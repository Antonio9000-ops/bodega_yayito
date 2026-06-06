class Producto:
    def __init__(self, id, nombre, sku, stock_actual, stock_minimo,
                 precio_venta, costo_promedio, categoria_id=None,
                 proveedor_id=None, unidad_id=None, fecha_vencimiento=None):
        self.id = id
        self.nombre = nombre
        self.sku = sku
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.precio_venta = precio_venta
        self.costo_promedio = costo_promedio
        self.categoria_id = categoria_id
        self.proveedor_id = proveedor_id
        self.unidad_id = unidad_id
        self.fecha_vencimiento = fecha_vencimiento

    def esta_en_stock_critico(self):
        return self.stock_actual <= self.stock_minimo

    def __str__(self):
        alerta = " ⚠️ CRÍTICO" if self.esta_en_stock_critico() else ""
        return f"[{self.sku}] {self.nombre} | Stock: {self.stock_actual} (mín: {self.stock_minimo}) | Precio: S/. {self.precio_venta:.2f}{alerta}"
