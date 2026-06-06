def validar_stock(stock_actual, cantidad_requerida):
    return stock_actual >= cantidad_requerida

def detectar_productos_criticos(lista_productos):
    return [p for p in lista_productos if p.stock_actual <= p.stock_minimo]

def valorizar_inventario(lista_productos):
    total = sum(p.stock_actual * p.costo_promedio for p in lista_productos)
    return round(total, 2)
