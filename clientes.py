import json
from datetime import datetime

# Archivos
INVENTARIO_FILE = "productos.json"
TICKETS_FILE = "tickets.json"

#carrito cliente
carrito = []

#funciones json
def cargar_productos():
    try:
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        #si el archivo no existe, crea un inventario inicial
        productos = [
            {"id": 1, "nombre": "Lapiz", "precio": 1000, "cantidad": 30},
            {"id": 2, "nombre": "Lapicero negro", "precio": 1000, "cantidad": 20},
            {"id": 3, "nombre": "Lapicero rojo", "precio": 1000, "cantidad": 20},
            {"id": 4, "nombre": "Borrador", "precio": 800, "cantidad": 20},
            {"id": 5, "nombre": "Sacapunta", "precio": 600, "cantidad": 20},
            {"id": 6, "nombre": "Cuaderno", "precio": 2500, "cantidad": 15},
            {"id": 7, "nombre": "Carpeta", "precio": 2000, "cantidad": 10},
            {"id": 8, "nombre": "Cartuchera", "precio": 4500, "cantidad": 10},
            {"id": 9, "nombre": "Pegante", "precio": 2000, "cantidad": 15},
            {"id": 10, "nombre": "Cinta", "precio": 2500, "cantidad": 12}
    
            ]
        guardar_productos(productos)
        return productos

def guardar_productos(productos):
    with open(INVENTARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

def guardar_ticket(ticket):
    try:
        with open(TICKETS_FILE, "r", encoding="utf-8") as f:
            tickets = json.load(f)
    except FileNotFoundError:
        tickets = []

    tickets.append(ticket)

    with open(TICKETS_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=4, ensure_ascii=False)

# -------- FUNCIONES DE TIENDA --------
def mostrar_productos(productos):
    print("\n📦 Lista de Productos:")
    print("ID  | Nombre          |Precio/u| Cantidad")
    print("-------------------------------------------")

    for p in productos:
        print(f"{p['id']:>2}  | {p['nombre']:<15} | {p['precio']:>6} | {p['cantidad']:>5}")

def buscar_producto(productos, producto_id):
    for p in productos:
        if p["id"] == producto_id:
            return p
    return None

def agregar_al_carrito(producto, cantidad):
    carrito.append({
        "nombre": producto["nombre"],
        "precio": producto["precio"],
        "cantidad": cantidad
    })
    producto["cantidad"] -= cantidad
    print(f"✅ {cantidad} unidad(es) de {producto['nombre']} añadidas al carrito.")

def ver_ticket():
    print("\n----- TICKET DE COMPRA -----")
    total = 0
    for item in carrito:
        subtotal = item["precio"] * item["cantidad"]
        total += subtotal
        print(f"{item['nombre']} x{item['cantidad']} = {subtotal} COP")
    print(f"\nTOTAL: {total} COP")
    print("Fecha:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-----------------------------")
    return {
        "items": carrito,
        "total": total,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# -------- FUNCIÓN PRINCIPAL --------
def tienda():
    productos = cargar_productos()
    print("\n🛒 Bienvenido a la Tienda Romay 🛒")
    mostrar_productos(productos)
    carrito.clear()

    while True:
        opcion = input("\n¿Qué producto desea comprar? (ID o escribe 'salir' para cancelar la compra): ").lower()
        if opcion == "salir":
            print("🛑 Compra cancelada.\n")
            return
        try:
            producto_id = int(opcion)
            producto = buscar_producto(productos, producto_id)
            if producto:
                while True:
                    try:
                        cantidad = int(input("¿Cuántas unidades desea?: "))
                        if cantidad <= 0:
                            print("Ingrese una cantidad mayor a cero (si está disponible).")
                        elif cantidad <= producto["cantidad"]:
                            agregar_al_carrito(producto, cantidad)
                            break
                        else:
                            print("❌ No hay suficiente stock.")
                    except ValueError:
                        print("❌ Ingrese un número por favor.")
            else:
                print("❌ Producto no encontrado.")
        except ValueError:
            print("❌ Entrada no válida.")

        while True:
            continuar = input("¿Desea agregar más productos? (s/n): ").lower()
            if continuar == 's':
                break
            elif continuar == "n":
                break
            else:
                print("Error. Seleccione (s/n) por favor.\n")

        if continuar == "n":
            break

    if carrito:
        ticket = ver_ticket()
        pagar = input("¿Desea pagar? (s/n): ").lower()
        if pagar == "s":
            guardar_ticket(ticket)
            guardar_productos(productos)
            print("✅ Gracias por su compra. Ticket guardado. \n")
        else:
            print("🛑 Compra cancelada. Se devuelve el stock. \n ")
            for item in carrito:
                for p in productos:
                    if p["nombre"] == item["nombre"]:
                        p["cantidad"] += item["cantidad"]
    else:
        print("No se agregó ningún producto.")

