"""
En este archivo se completan las funciones que son utilizadas para
la creación de la lista de reproducción
"""
from functools import reduce

from usuario import Usuario


def filtrar_prohibidos(iterar_peliculas, actor_prohibido):
    """
    Debe filtrar todas películas  que contengan temas prohibidos
    :param actor_prohibido: actor prohibido del usuario
    :param iterar_peliculas: iterador sobre lista de Videos
    :return: filter
    """
    return filter(lambda x: actor_prohibido not in x.actores, iterar_peliculas)

def calcular_afinidades(catalogo_peliculas, usuario: Usuario):
    """
    La función debe calcular las afinidades según preferencias del usuario.
    El map retorna tuplas, donde el primer valor es la pelicula,
    y el segundo valor la afinidad.
    :param usuario: Usuario para quien se crearán las afinidades
    :param catalogo_peliculas: zip que retorna peliculas
    :return: mapeo que retorna tuplas.
    """
    return map(lambda x: (x, usuario.calcular_afinidad(x)), catalogo_peliculas)

def encontrar_peliculas_comunes(usuarios_watch_party):
    """
    La función debe encontrar las películas comunes entre las favoritas
    de cada usuario, y retornar un set que las contenga.
    :param usuarios_watch_party: lista de usuarios que conforman la watch party
    :return: interseccion de las peliculas favoritas de cada usuario
    """
    print("encontrar()")
    print(usuarios_watch_party)
    favorite_movies = map(lambda x: x.peliculas_favoritas, usuarios_watch_party)
    return reduce(lambda x, y: x & y, favorite_movies)

def encontrar_usuario_mas_afin(usuario, otros_usuarios):
    """
    Esta función debe encontrar el usuario con mayor compatibilidad.
    Debe primero filtrar usuarios que no tengan el mismo actor_prohibido,
    y luego encontrar aquél con quien tenga mayor compatibilidad
    :param usuario: usuario para quien se encontrará un amigue
    :param otros_usuarios: el resto de los usuarios de DCCabritas
    :return: Usuario más compatible
    """
    filtered_users = filter(lambda x: usuario.actor_prohibido == x.actor_prohibido, otros_usuarios)
    return max(map(lambda x: (x + usuario, usuario), filtered_users), key=lambda x: x[0])[1]
