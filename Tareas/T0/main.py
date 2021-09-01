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
posts = csv.readCsv("publicaciones.csv", 5)

comments_array = csv.readCsv("comentarios.csv", 3)
comments = {data[1]: data for data in comments_array[1:]}

users_array = csv.readCsv("usuarios.csv", 0)
users = {user[0] for user in users_array[1:]}


menu_state = Menu.start
logged_in = False
# No hay switch en Python :(
while True:
    options = dict()
    if menu_state == Menu.start:
        print("Bienvenidos a DCCommerce!\n")
        print("Que desea hacer?")

        options = {
                "a": ("Ingresar como usuario registrado", 0),
                "s": ("Ingresar como usuario anónimo", Menu.posts),
                "w": ("Volver al menú anterior", 0),
                "q": ("Salir de DCComemerce", Menu.exit)
                }

    elif menu_state == Menu.exit:
        print("Gracias por usar DCComerce, hasta pronto!")
        break

    elif menu_state == 1:
        pass
    elif menu_state == 1:
        pass
    elif menu_state == 1:
        pass

    while True:
        for option in options:
            print(f"[{option}] - {options[option][0]} ")

        user_input = input("INPUT: ").strip()
        print("")
        if user_input not in options:
            print("Comando no válido, intentelo nuevamente")
        else:
            menu_state = options[user_input][1]
            break
