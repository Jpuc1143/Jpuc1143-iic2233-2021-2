import parametros
import csvUtils as csv

# Cargar todos los csv
posts = csv.readCsv("publicaciones.csv", 5)

comments_array = csv.readCsv("comentarios.csv", 3)
comments = {data[1]: data for data in comments_array[1:]}

users_array = csv.readCsv("usuarios.csv", 0)
users = set(user[0] for user in users_array[1:])

# TODO: main loop
