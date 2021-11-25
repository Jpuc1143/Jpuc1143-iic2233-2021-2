from collections import deque


class NodoGrafo:
    def __init__(self, usuario):
        # No modificar
        self.usuario = usuario
        self.amistades = None

    def formar_amistad(self, nueva_amistad):
        # amistades no es un set :( x2
        if nueva_amistad not in self.amistades:
            self.amistades.append(nueva_amistad)
        if self not in nueva_amistad.amistades:
            nueva_amistad.amistades.append(self)

    def eliminar_amistad(self, ex_amistad):
        if ex_amistad in self.amistades:
            self.amistades.remove(ex_amistad)
        if self in ex_amistad.amistades:
            ex_amistad.amistades.remove(self)


def recomendar_amistades(nodo_inicial, profundidad):
    """
    Recibe un NodoGrafo inicial y una profundidad de busqueda, retorna una
    lista de nodos NodoGrafo recomendados como amistad a esa profundidad.
    """

    def explore_friends(current_node, depth):
        if depth <= 1:
            return set(current_node.amistades)
        else:
            friends = set()
            for node in current_node.amistades:
                friends.update(explore_friends(node, depth - 1))
            return friends

    print(f"iniciando busqueda, {nodo_inicial} {profundidad}")
    possible_friends = explore_friends(nodo_inicial, profundidad + 1)
    possible_friends -= set(nodo_inicial.amistades)
    return possible_friends


def busqueda_famosos(nodo_inicial, visitados=None, distancia_max=80):
    """
    [BONUS]
    Recibe un NodoGrafo y busca en la red social al famoso mas
    cercano, retorna la distancia y el nodo del grafo que contiene
    a el usuario famoso cercano al que se encuentra.
    """
    visited = set()
    processing = deque()
    processing.append((0, nodo_inicial))
    visited.add(nodo_inicial)

    while True:
        try:
            data = processing.popleft()
        except IndexError:
            return (distancia_max, None)

        node = data[1]
        depth = data[0]
        if node.usuario.es_famoso:
            return data
        elif depth >= distancia_max:
            return (distancia_max, None)
        else:
            for subnode in node.amistades:
                if subnode not in visited:
                    processing.append((depth+1, subnode))
                    visited.add(subnode)
