from enum import Enum, auto

import parametros
import csvUtils as csv

# TODO: Citar codigo de enum https://docs.python.org/3/library/enum.html?highlight=enum
class Menu(Enum):
    start = auto()
    main = auto()
    posts = auto()
    view_post = auto()
    exit = auto()
    login = auto()

# Cargar todos los csv
posts = csv.readCsv("publicaciones.csv", 5)[1:]

comments_array = csv.readCsv("comentarios.csv", 3)
comments = {data[1]: data for data in comments_array[1:]}

users_array = csv.readCsv("usuarios.csv", 0)
users = {user[0] for user in users_array[1:]}


menu_state = Menu.start
logged_in = False
current_post = None
# No hay switch en Python :(
while True:
    options = dict()
    if menu_state == Menu.start:
        logged_in = False
        print("Bienvenidos a DCCommerce!\n")
        print("Que desea hacer?")

        options = {
            "a": ("Ingresar como usuario registrado", Menu.login),
            "s": ("Ingresar como usuario anónimo", Menu.posts),
            "w": ("Volver al menú anterior", 0),
            "q": ("Salir de DCComemerce", Menu.exit)
                }

    elif menu_state == Menu.exit:
        print("Gracias por usar DCComerce, hasta pronto!")
        break

    elif menu_state == Menu.login:
        print("ANUNCIO: no se preocupe estimados clientes,\n"
            "en las proximas versiones de DCCommerce se va a requerir una contraseña;\n"
            "hasta entonces respete el codigo de honor.")
        user_input = input("Ingrese su usuario: ")
        
        if user_input in users:
            logged_in = True
            menu_state = Menu.posts
            print("Ha ingresado con éxito a DCCommerce!")
        else:
            menu_state = Menu.start
            print("ERROR: usuario no existe")

        continue

    elif menu_state == Menu.posts:
        print("Lista de publicaciones:\n")

        if logged_in:
            options = {"w": ("Volver al menú anterior", Menu.main)}
        else:
            options = {"w": ("Volver al menú anterior", Menu.start)}
        options["q"] = ("Salir de DCCommerce", Menu.exit)

        for post in reversed(posts):
            options[post[0]] = (f"{post[1]} (${post[4]})", Menu.view_post)


    elif menu_state == Menu.view_post:
        post = posts[current_post]
        print(f"ID: {post[0]}")
        print(f"Nombre: {post[1]}")
        print(f"Precio: ${post[4]}")
        print(f"Vendedor: {post[2]}")
        print(f"Fecha de Publicación: {post[3]}")
        print(f"Descripción:\n{post[5]}\n")

        print("Comentarios:")
        print("TODO")

        options = {
            "q": ("Salir de DCCommerce", Menu.exit),
            "w": ("Volver al menú anterior", Menu.posts)
            }
            
        if current_post != 0:
            options["a"] = ("Ver publicación anterior", Menu.view_post)
        if current_post != len(posts) - 1:
            options["d"] = ("Ver siguiente publicación", Menu.view_post)


    elif menu_state == None:
        print("You done goofed") # TODO: hacer esto más formal
        exit()

    while True:
        for option in options:
            print(f"[{option}] - {options[option][0]} ")

        user_input = input("INPUT: ").strip()
        print("")
        if user_input not in options:
            print("Comando no válido, intentelo nuevamente")

        else:
            if menu_state == Menu.posts and user_input.isnumeric():
                current_post = int(user_input) - 1 
            if menu_state == Menu.view_post:
                if user_input == "a":
                    current_post -= 1
                elif user_input == "d":
                    current_post += 1

            menu_state = options[user_input][1]
            break
