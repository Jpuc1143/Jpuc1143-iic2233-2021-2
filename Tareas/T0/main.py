import csv_utils as csv
from parametros import Menu
from user_actions import publish_comment, register_user, find_self_posts, publish_post, delete_post

if __name__ == "__main__":
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

    menu_state = Menu.START
    logged_in = False
    current_user = None
    current_post = None
    show_only_self_posts = False
    shown_posts = None

    # No hay switch en Python :(
    while True:
        options = dict()
        if menu_state == Menu.START:
            logged_in = False
            current_user = None

            print("Bienvenidos a DCCommerce!\n")
            print("Que desea hacer?")

            options = {
                "a": ("Ingresar como usuario registrado", Menu.LOGIN),
                "s": ("Ingresar como usuario anónimo", Menu.POSTS),
                "d": ("Registrarse como un nuevo usuario", Menu.REGISTER),
                "q": ("Salir de DCComemerce", Menu.EXIT)
                    }

        elif menu_state == Menu.EXIT:
            print("Gracias por usar DCComerce, hasta pronto!")
            break

        elif menu_state == Menu.REGISTER:
            print(f"El nombre de usuario no puede tener más de {MAX_CARACTERES}, menos de {MIN_CARACTERES} o una ','")
            user_name = input("Ingrese su nuevo nombre de usuario: ")
            if user_name == "":
                menu_state = Menu.START
            else:
                if register_user(user_name, users):
                    logged_in = True
                    current_user = user_name
                    menu_state = Menu.MAIN
                else:
                    print("ERROR: Este no es un nombre de usuario valido o ya existe.")

            continue

        elif menu_state == Menu.LOGIN:
            print("ANUNCIO: no se preocupe estimados clientes,\n"
                  "en las proximas versiones de DCCommerce se va a requerir una contraseña;\n"
                  "hasta entonces respete el codigo de honor.")
            user_input = input("Ingrese su usuario: ")

            if user_input in users:
                logged_in = True
                current_user = user_input
                menu_state = Menu.MAIN
                print("")
            else:
                menu_state = Menu.START
                print("ERROR: usuario no existe")

            continue

        elif menu_state == Menu.POSTS:
            if show_only_self_posts:
                shown_posts = find_self_posts(current_user, posts)
            else:
                shown_posts = []
                for post in posts:
                    if post is not None:
                        shown_posts.append(post)

            print("Lista de publicaciones:\n")

            options = dict()
            if len(shown_posts) == 0:
                print("No hay publicaciones disponibles")
            else:
                for post in reversed(shown_posts):
                    if post is not None:
                        options[post[0]] = (f"{post[1]} (${post[4]})", Menu.VIEW_POST)

            if logged_in:
                options["s"] = ("Crear publicación", Menu.PUBLISH_POST)
                options["w"] = ("Volver al menú anterior", Menu.MAIN)
            else:
                options["w"] = ("Volver al menú anterior", Menu.START)

            options["q"] = ("Salir de DCCommerce", Menu.EXIT)

        elif menu_state == Menu.VIEW_POST:
            post = posts[current_post]
            
            print(f"Nombre: {post[1]}")
            print(f"ID: {post[0]}")
            print(f"Precio: ${post[4]}")
            print(f"Vendedor: {post[2]}")
            print(f"Fecha de Publicación: {post[3]}")
            print(f"Descripción:\n{post[5]}\n")

            print("Comentarios:")
            if post[0] in comments:
                for comment in comments[post[0]]:
                    print(f"{comment[2]} <{comment[1]}> {comment[3]}")
            else:
                print("No hay comentarios")
            print("")

            options = dict()
            if logged_in:
                options["s"] = ("Publicar comentario", Menu.PUBLISH_COMMENT)

            if current_post != int(shown_posts[0][0]) - 1:
                options["a"] = ("Ver publicación anterior", Menu.VIEW_POST)
            if current_post != int(shown_posts[-1][0]) - 1:
                options["d"] = ("Ver siguiente publicación", Menu.VIEW_POST)

            if current_user == post[2]:
                options["x"] = ("Eliminar publicación",  Menu.DELETE_POST)

            options["w"] = ("Salir de DCCommerce", Menu.EXIT)
            options["q"] = ("Volver al menú anterior", Menu.POSTS)

        elif menu_state == Menu.MAIN:
            show_only_self_posts = False
            print(f"Bienvenido {current_user}!")

            options = {
                "a": ("Ver todas las publicaciones", Menu.POSTS),
                "s": ("Ver publicaciones realizadas", Menu.SELF_POSTS),
                "w": ("Log out", Menu.START),
                "q": ("Salir de DCCommerce", Menu.EXIT)
                    }

        elif menu_state == Menu.SELF_POSTS:
            show_only_self_posts = True
            menu_state = Menu.POSTS
            continue

        elif menu_state == Menu.PUBLISH_COMMENT:
            print("Escriba su comentario. Deje vacio para cancelar:")
            comment_text = input()
            if comment_text is not "":
                publish_comment(comment_text, current_user, current_post, comments)

            menu_state = Menu.VIEW_POST
            continue

        elif menu_state == Menu.PUBLISH_POST:
            print("Ingrese la información de su publicacion. Deje vacio para cancelar.")
            title = input("Título: ")
            if title is "":
                menu_state = Menu.POSTS
                continue

            price = input("Precio: ")
            while True:
                if price.isnumeric or price is "":
                    break
                else:
                    price = input("El precio debe ser un número: ")

            if price is "":
                menu_state = Menu.POSTS
                continue

            desc = input("Descripción: ")
            if desc is "":
                menu_state = Menu.POSTS
                continue

            current_post = publish_post(title, price, desc, current_user, posts)
            if show_only_self_posts:
                shown_posts = find_self_posts(current_user, posts)
            menu_state = Menu.VIEW_POST
            continue

        elif menu_state == Menu.DELETE_POST:
            if input("¿Está seguro? (\"si\" para continuar): ").casefold() == "si":
                delete_post(current_post, posts, comments)
                menu_state = Menu.POSTS
            else:
                menu_state = Menu.VIEW_POST
            continue

        while True:
            for option in options:
                print(f"[{option}] - {options[option][0]} ")

            user_input = input("INPUT: ").strip()
            print("")
            if user_input not in options:
                print("ERROR: Comando no válido, intentelo nuevamente")

            else:
                if menu_state == Menu.POSTS and user_input.isnumeric():
                    current_post = int(user_input) - 1
                if menu_state == Menu.VIEW_POST:
                    if user_input == "a":
                        index = shown_posts.index(posts[current_post])
                        current_post = int(shown_posts[index - 1][0]) - 1

                    elif user_input == "d":
                        index = shown_posts.index(posts[current_post])
                        current_post = int(shown_posts[index + 1][0]) - 1

                menu_state = options[user_input][1]
                break
