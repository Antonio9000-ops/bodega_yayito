from services.inventario_service import BodegaController

def menu():
    print("===== BODEGA YAYITO - SISTEMA ERP =====")
    print("1. Registrar nuevo producto")
    print("2. Realizar movimiento (entrada/salida)")
    print("3. Ver productos críticos")
    print("4. Salir")
    return input("Opción: ")

if __name__ == "__main__":
    controller = BodegaController()
    while True:
        op = menu()
        if op == "1":
            # Datos ficticios, puedes pedir inputs o usar widgets
            print("Función de registro pendiente de implementar con inputs")
        elif op == "2":
            print("Función de movimiento pendiente")
        elif op == "3":
            controller.ver_estado_critico()
        elif op == "4":
            break
        else:
            print("Opción inválida")
