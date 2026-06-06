from models.movimiento_model import registrar_movimiento as registrar_movimiento_db
from utils.validators import validar_stock

class Movimiento:
    TIPOS_VALIDOS = ('ENTRADA', 'SALIDA')

    def __init__(self, producto, tipo_movimiento, cantidad, costo_operacion, motivo):
        self.producto = producto
        self.tipo_movimiento = tipo_movimiento.upper().strip()
        self.cantidad = cantidad
        self.costo_operacion = costo_operacion
        self.motivo = motivo

    def validar(self):
        if self.tipo_movimiento not in self.TIPOS_VALIDOS:
            return False, f"Tipo '{self.tipo_movimiento}' inválido. Use ENTRADA o SALIDA."
        if self.cantidad <= 0:
            return False, "La cantidad debe ser positiva."
        if self.costo_operacion < 0:
            return False, "El costo no puede ser negativo."
        if self.tipo_movimiento == 'SALIDA':
            if not validar_stock(self.producto.stock_actual, self.cantidad):
                return False, f"Stock insuficiente. Disponible: {self.producto.stock_actual}, solicitado: {self.cantidad}"
        return True, "Válido"

    def ejecutar(self):
        valido, msg = self.validar()
        if not valido:
            print(f"❌ Movimiento rechazado: {msg}")
            return False, msg
        try:
            registrar_movimiento_db(self.producto.id, self.tipo_movimiento,
                                    self.cantidad, self.costo_operacion, self.motivo)
            if self.tipo_movimiento == 'ENTRADA':
                self.producto.stock_actual += self.cantidad
            else:
                self.producto.stock_actual -= self.cantidad
            return True, f"Movimiento {self.tipo_movimiento} registrado."
        except Exception as e:
            return False, f"Error en BD: {e}"
