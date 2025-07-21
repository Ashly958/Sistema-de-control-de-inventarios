import json
# se trabaja con .json para tratar de manera permanente los datos
# with open abre, edita y cierra el archivo .json

def autenticar_usuario():
    intentos = 3  
    while intentos > 0:
        print("\n--- INGRESE SUS CREDENCIALES --- \n Recuerde ingresar los espacios correctamente. ")
        usuario = input("Usuario: ").lower().strip()  # .strip() = elimina espacios adicionales. .lower() = todo en minúsculas
        contraseña = input("Contraseña: ").strip()
        
        with open('usuarios.json', 'r') as archivo: # abre y lee el usuarios.json
            usuarios = json.load(archivo) # se guarda en la variable usuarios
            
        if usuario in usuarios and usuarios[usuario] == contraseña: # verifica credenciales
            print("\n--- BIENVENIDO AL SISTEMA DE ADMINISTRACIÓN ---")
            return True  # retorna True cuando la autenticación es exitosa

        intentos -= 1 # descuenta 1 intento
        print("\nCredenciales incorrectas.")
        if intentos > 0: # si intentos es mayor a 0 puede seguir intentando ingresar al sistema
            print(f"Intentos restantes: {intentos}")
        else: # sino, se acaba el programa
            print("\nHa agotado sus intentos. Saliendo del sistema...")
    return False  # termina la función y retorna a main

def cambiar_clave():
    user = input("\n Ingrese su usuario:")
    with open('usuarios.json', 'r') as archivo: # abre y lee usuarios como la variable archivo
        usuarios = json.load(archivo) # se alamacena en usuarios
    if user in usuarios:
        nueva_clave = input("Ingrese su nueva contraseña: ")
        usuarios[user] = nueva_clave #actualiza la clave user con el valor nueva_clave
        with open('usuarios.json', 'w') as archivo: # borra lo que estaba y escribe los cambios hechos en la clave [user]
            json.dump(usuarios, archivo, indent=4) # .dump "empuja" los cambios realizados
        print("\n Contraseña actualizada exitosamente.") 
        return menu_admin()
    else:
        print("Usuario no encontrado. No se pudo cambiar la contraseña. ")

def agregar_usuario():
    user = input("\n Ingrese el nombre del nuevo usuario: ")
    with open('usuarios.json', 'r') as archivo: # abre y lee
        usuarios = json.load(archivo)
    if user in usuarios:
        print("El usuario ya existe. No se pudo agregar.")
    else:
        contraseña = input("Ingrese la contraseña para el nuevo usuario: ")
        usuarios[user] = contraseña # valor para la clave user
        with open('usuarios.json', 'w') as archivo: # escribe lo hecho
            json.dump(usuarios, archivo, indent=4) # empuja los cambios
        print("Usuario agregado exitosamente. <3")
        return menu_admin()

def eliminar_usuario():
    user = input("Ingrese el nombre del usuario que desea eliminar: ")
    with open('usuarios.json', 'r') as archivo:  # abre y lee
        usuarios = json.load(archivo) #.load lee el archivo .json y lo convierrte a un diccionario para que python entienda
    if user in usuarios:
        del usuarios[user]
        with open('usuarios.json', 'w') as archivo:
            json.dump(usuarios, archivo, indent=4)
        print("Usuario eliminado exitosamente.")
        return menu_admin()
    else:
        print("Usuario no encontrado. No se puede eliminar usuario que no existen.")
        return menu_admin()

def mostrar_usuarios():
    print("\n ✩ Lista de usuarios ✩ \n")
    with open('usuarios.json', 'r') as archivo: # abre y lee
        usuarios = json.load(archivo)
    for user, contraseña in usuarios.items(): # items = (clave - valor)
        print(f" • Usuario: {user}, Contraseña: {contraseña}") # separa la clave en user y el valor en contraseña
    return   

def mostrar_inventario():
    print('\n----- INVENTARIO DE PRODUCTOS DE LA TIENDA ROMAY 📝​ ----\n')
    with open('productos.json', 'r') as archivo: #abre y lee productos
        productos = json.load(archivo) 
    for producto in productos: # producto = variable de indentacion
        print(f'Id :{producto["id"]} | Nombre : {producto["nombre"]} | Precio : {producto["precio"]} | Cantidad : {producto["cantidad"]}') # saca la clave " " y imprime

def registrar_venta():
    print("\n ➤ ----- REGISTRO DE VENTAS AHORA ----- \n")
    try:
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo)
        # cada <n es un espacio guardado en la terminal y ubica en ese espacio
        print("{:<5} {:<20} {:<10} {:<10}".format("ID", "Producto", "Precio", "Stock"))
        print("-" * 45)
        for p in productos: # p = variable de indentacion
            print("{:<5} {:<20} ${:<9} {:<10}".format(p["id"], p["nombre"], p["precio"], p["cantidad"]))
            # format ubica los valores de id, nombre y demas y los pone en n
        producto_nombre = input("\nIngrese el nombre del producto vendido: ").strip().lower()
        cantidad = int(input("Ingrese la cantidad vendida: "))

        producto_encontrado = None # aun no ha encontrado nada porque es una variable vacia
        for p in productos:
            if p["nombre"].lower() == producto_nombre:
                producto_encontrado = p
                break
        if not producto_encontrado:
            print("\n Error: Producto no encontrado")
            return menu_admin()
        
        if producto_encontrado["cantidad"] < cantidad: # Valida stock
            print("\n Error: No hay suficiente stock")
            print(f"Stock disponible: {producto_encontrado['cantidad']}")
            return menu_admin()
            
        if cantidad <= 0:
            print("\n Error: La cantidad debe ser mayor a cero")
            return menu_admin()
            
        producto_encontrado["cantidad"] -= cantidad # actualiza el stock

        with open('productos.json', 'w') as archivo: # guarda todo
            json.dump(productos, archivo, indent=4)
            
        print(f"\n✅ Venta registrada: {cantidad} unidades de {producto_encontrado['nombre']}")
        print(f"Stock restante: {producto_encontrado['cantidad']}")
        return menu_admin()
        
    except ValueError:
        print("\n Error: Ingrese una cantidad válida (número entero)")
        return menu_admin()
    except Exception as e: 
        print(f"\n Error inesperado: {str(e)}")
        return menu_admin()

def agregar_nueva_mercancia():
    print("\n ✿ ----- AGREGAR NUEVA MERCANCÍA ----- ✿ \n")
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    cantidad = int(input("Ingrese la cantidad del producto: "))
    with open('productos.json', 'r') as archivo: # abre y lee
        productos = json.load(archivo)
    nuevo_producto = {
        "id": len(productos) + 1,
        "nombre": nombre, #estructura
        "precio": precio,
        "cantidad": cantidad
    }
    productos.append(nuevo_producto)
    with open('productos.json', 'w') as archivo: # escribe y empuja
        json.dump(productos, archivo, indent=4)
    print(f"Producto {nombre} agregado exitosamente al inventario. \n")
    return menu_admin()

def actualizar_cantidades():
    print("\n ★ ----- ACTUALIZAR CANTIDADES DE LOS PRODUCTOS ----- ★ \n")
    opcion = input ("1. Actualizar cantidades de todos los productos\n2. Actualizar cantidad de un producto específico\nSeleccione una opción: ")
    
    if opcion == '1':
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo) # abre y lee
        for producto in productos:
            nueva_cantidad = int(input(f"Ingrese la nueva cantidad para {producto['nombre']} (actual: {producto['cantidad']}): "))
            producto['cantidad'] = nueva_cantidad # cambia el valor de la clave cantidad
        with open('productos.json', 'w') as archivo: # escribe y empuja
            json.dump(productos, archivo, indent=4)
        print("Cantidades actualizadas exitosamente.")
        return menu_admin()
    
    elif opcion == '2':
        nombre = input("Ingrese el nombre del producto: ")
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo)
        encontrado = False
        for producto in productos:
            if producto['nombre'].lower() == nombre.lower():
                nueva_cantidad = int(input(f"Ingrese la nueva cantidad para {producto['nombre']} (actual: {producto['cantidad']}): "))
                producto['cantidad'] = nueva_cantidad
                encontrado = True
                break
        if encontrado == True:
            with open('productos.json', 'w') as archivo:
                json.dump(productos, archivo, indent=4)
            print("Cantidad actualizada exitosamente.")
            return menu_admin()
        else:
            print("Producto no encontrado en el inventario.")
    else:
        print("Opción no válida. Por favor, intente de nuevo.")

def actualizar_precios():
    print("\n  ⋆ ----- ACTUALIZAR PRECIO DE LOS PRODUCTOS ----- ⋆ \n ")
    opcion = input ("1. Actualizar los precios de todos los productos\n2. Actualizar el precio de un producto específico\nSeleccione una opción: ")
    
    if opcion == '1':
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo) # abre y lee
        for producto in productos:
            nuevo_precio = int(input(f"Ingrese el nuevo precio para {producto['nombre']} (actual: {producto['precio']}): "))
            producto['precio'] = nuevo_precio # reemplaza
        with open('productos.json', 'w') as archivo:
            json.dump(productos, archivo, indent=4) # empuja
        print("Precios actualizados exitosamente.")
        return menu_admin()
    
    elif opcion == '2':
        nombre = input("Ingrese el nombre del producto: ")
        with open('productos.json', 'r') as archivo:
            productos = json.load(archivo) # abre y lee
        encontrado = False
        for producto in productos:
            if producto['nombre'].lower() == nombre.lower():
                nuevo_precio = int(input(f"Ingrese el nuevo precio para {producto['nombre']} (actual: {producto['precio']}): "))
                producto['precio'] = nuevo_precio
                encontrado = True
                break
        if encontrado == True:
            with open('productos.json', 'w') as archivo: # empuja
                json.dump(productos, archivo, indent=4)
            print("Precio actualizado exitosamente.")
            return menu_admin()
        else:
            print("Producto no encontrado en el inventario.")
    else:
        print("Opción no válida. Por favor, intente de nuevo.")

def eliminar_productos():
    nombre = input("Ingrese el nombre del producto que desea eliminar: ")
    with open('productos.json', 'r') as archivo:
        productos = json.load(archivo) # abre y lee
    producto_encontrado = False
    for i, producto in enumerate(productos):
        if producto['nombre'].lower() == nombre.lower():
            del productos[i] 
            producto_encontrado = True
            break
    if producto_encontrado == True:
        with open('productos.json', 'w') as archivo:
            json.dump(productos, archivo, indent=4) # empuja
        print("Producto eliminado exitosamente.")
        return menu_admin()
    else:
        print("Producto no encontrado. No se pueden eliminar productos que no existen.")

def mostrar_ventas(): 
    print("\n --- REGISTRO DE VENTAS HASTA EL MOMENTO --- \n")
    with open('tickets.json', 'r') as archivo:
        tickets = json.load(archivo)  # abre y lee
    for ticket in tickets:
        print(f"Fecha: {ticket['fecha']} | Total: {ticket['total']}")
        print("Productos vendidos:")
        for item in ticket["items"]:
            print(f" - {item['nombre']} | Precio: {item['precio']} | Cantidad: {item['cantidad']}")
        print("-" * 50)  
    return registrar_venta()


def menu_admin():
    opcion = input("\n ♡ --- MENÚ DE ADMINISTRADOR --- ♡ \n 1. Ver inventario. \n 2. Ventas. \n 3. Administrar información de inicio de sesión. \n 4. SALIR \n Seleccione una opción:   ")
    
    if opcion == '1': 
        mostrar_inventario()
        op_1 = input ("\n ♡ --- MENÚ DE INVENTARIO --- ♡ \n 1. Registrar nueva mercancia. \n 2. Actualizar cantidades. \n 3. Actualizar precios. \n 4. Eliminar productos. \n 5. Volver a menú de admin. \n Seleccione una opción: ")
        if op_1 == '1':
            agregar_nueva_mercancia()
        elif op_1 == '2':
            actualizar_cantidades()
        elif op_1 == '3':
            actualizar_precios()
        elif op_1 == '4':
            eliminar_productos()
        elif op_1 == '5':
            print ("Saliendo del menú de inventario...")
            return menu_admin()
        else: 
            print ("Opción no válida.")

    elif opcion == '2':
        print("\n --- VENTAS --- \n ")
        mostrar_ventas()
        registrar_venta()
        input("\nPresione Enter para continuar...")

    elif opcion == '3':
        mostrar_usuarios()
        op = input("\n ♡ --- Menú de administracion de inicio de sesión --- ♡ \n 1. Agregar usuario. \n 2. Cambiar clave. \n 3. Eliminar usuario. \n Seleccione una opción: ")
        if op == '1':
            agregar_usuario()
        elif op == '2':
            cambiar_clave()
        elif op == '3':
            eliminar_usuario()
        else: 
            print("Opción no válida.")
            return
        

    elif opcion == '4':
        print ("Saliendo del programa...")

    else:
        print ("Opción no válida.")
        
