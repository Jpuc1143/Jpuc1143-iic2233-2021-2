from enum import Enum, auto

import parametros
import csvUtils as csv
from userActions import publish_comment, register_user, find_self_posts

# TODO: Citar codigo de enum https://docs.python.org/3/library/enum.html?highlight=enum
class Menu(Enum):
    start = auto()
    main = auto()
    posts = auto()
    view_post = auto()
    exit = auto()
    login = auto()
    PUBLISH_COMMENT = auto()
    REGISTER = auto()
    SELF_POSTS = auto()

# Cargar todos los csv
posts = csv.read_csv("publicaciones.csv", 5)[1:]

comments_array = csv.read_csv("comentarios.csv", 3)
comments = dict()
for comment in comments_array[1:]:
    if comment[0] not in comments:
        comments[comment[0]] = [comment]
    else:
        comments[comment[0]].append(comment)

users_array = csv.read_csv("usuarios.csv", 0)
users = {user[0] for user in users_array[1:]}


menu_state = Menu.start
logged_in = False
current_user = None
current_post = None
show_only_self_posts = False
shown_posts = None

# No hay switch en Python :(
while True:
    options = dict()
    if menu_state == Menu.start:
        logged_in = False
        current_user = None

        print("Bienvenidos a DCCommerce!\n")
        print("Que desea hacer?")

        options = {
            "a": ("Ingresar como usuario registrado", Menu.login),
            "s": ("Ingresar como usuario anónimo", Menu.posts),
            "d": ("Registrarse como un nuevo usuario", Menu.REGISTER),
            "q": ("Salir de DCComemerce", Menu.exit)
                }

    elif menu_state == Menu.exit:
        print("Gracias por usar DCComerce, hasta pronto!")
        break

    elif menu_state == Menu.REGISTER:
        print("TODO")
        user_name = input("Ingrese su nuevo nombre de usuario. Este no puede TODO: ")
        if user_name == "":
            menu_state = Menu.start
        else:
            if register_user(user_name, users):
                logged_in = True
                current_user = user_name
                menu_state = Menu.main
            else:
                print("Este no es un nombre de usuario valido o ya existe")

        continue

    elif menu_state == Menu.login:
        print("ANUNCIO: no se preocupe estimados clientes,\n"
            "en las proximas versiones de DCCommerce se va a requerir una contraseña;\n"
            "hasta entonces respete el codigo de honor.")
        user_input = input("Ingrese su usuario: ")
        
        if user_input in users:
            logged_in = True
            current_user = user_input
            menu_state = Menu.main
            print("")
        else:
            menu_state = Menu.start
            print("ERROR: usuario no existe")

        continue

    elif menu_state == Menu.posts:
        if show_only_self_posts:
            shown_posts = find_self_posts(current_user, posts)
        else:
            shown_posts = posts
        
        print("Lista de publicaciones:\n")

        if logged_in:
            options = {"w": ("Volver al menú anterior", Menu.main)}
        else:
            options = {"w": ("Volver al menú anterior", Menu.start)}
        options["q"] = ("Salir de DCCommerce", Menu.exit)

        for post in reversed(shown_posts):
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
        for comment in comments[post[0]]:
            print(f"{comment[2]} <{comment[1]}> {comment[3]}")
        print("")

        options = {
            "q": ("Salir de DCCommerce", Menu.exit),
            "w": ("Volver al menú anterior", Menu.posts)
            }
        
        if current_post != int(shown_posts[0][0]) - 1:
            options["a"] = ("Ver publicación anterior", Menu.view_post)
        if current_post != int(shown_posts[-1][0]) - 1:
            options["d"] = ("Ver siguiente publicación", Menu.view_post)

        if logged_in:
            options["s"] = ("Publicar comentario", Menu.PUBLISH_COMMENT)

    elif menu_state == Menu.main:
        show_only_self_posts = False
        print(f"Bienvenido de vuelta {current_user}!")

        options = {
            "a": ("Ver todas las publicaciones", Menu.posts),
            "s": ("Ver publicaciones realizadas", Menu.SELF_POSTS),
            "w": ("Log out", Menu.start),
            "q": ("Salir de DCCommere", Menu.exit)
                }

    elif menu_state == Menu.SELF_POSTS:
        show_only_self_posts = True
        menu_state = Menu.posts
        continue

    elif menu_state == Menu.PUBLISH_COMMENT:
        print("Escriba su comentario. Deje vacio para cancelar:")
        comment_text = input()
        if comment_text is not "":
            publish_comment(comment_text, current_user, current_post, comments)

        menu_state = Menu.view_post
        continue

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
                    index = shown_posts.index(posts[current_post])
                    current_post = int(shown_posts[index - 1][0]) - 1

                elif user_input == "d":
                    index = shown_posts.index(posts[current_post])
                    current_post = int(shown_posts[index + 1][0]) - 1

            menu_state = options[user_input][1]
            break
