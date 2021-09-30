"""
En este archivo se encuentra la clase ListaReproduccion, la Iterable que
contiene los videos ordenados
"""


class ListaReproduccion:

    def __init__(self, conjunto_videos, usuario, nombre):
        self.conjunto_videos = conjunto_videos
        self.usuario = usuario
        self.nombre = nombre

    def __iter__(self):
        return IterarLista(self.conjunto_videos.copy())

    def __str__(self):
        return f"Lista de Reproducción de {self.usuario}: {self.nombre}"


class IterarLista:

    def __init__(self, conjunto_videos):
        self.conjunto_videos = conjunto_videos

    def __iter__(self):
        return self

    def __next__(self):
        if self.conjunto_videos:
            next_movie = max(self.conjunto_videos, key=lambda x: x[1])
            self.conjunto_videos.remove(next_movie)
            return next_movie[0]
            
        else:
            raise StopIteration
