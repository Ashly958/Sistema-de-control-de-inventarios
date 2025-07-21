from admin import menu_admin, autenticar_usuario
from clientes import tienda

while True:
    print("\n----- Sistema de Simulación de Inventarios -----")
    print("\n ​​🛒​ BIENVENIDO A LA TIENDA ROMAY \n")
    print("¿Quién eres?\n")
    opcion = input (" 1. Cliente \n 2. Administrador \n 3. Salir \n Elige una opción: ")
    if opcion == '1':
        tienda()
    elif opcion == '2':
        if autenticar_usuario() == True:
            menu_admin()
    elif opcion == '3':
        print ("Saliendo del programa...")
        break 
    else:
        print(" Opción inválida. \n Saliendo del sistema. ¡Bye Bye!")
        break