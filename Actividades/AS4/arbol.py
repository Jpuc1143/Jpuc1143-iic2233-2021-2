class NodoFama:

    def __init__(self, usuario, padre=None):
        # No modificar
        self.usuario = usuario
        self.padre = padre
        self.hijo_izquierdo = None
        self.hijo_derecho = None


class ArbolBinario:

    def __init__(self):
        # No modificar
        self.raiz = None

    def crear_arbol(self, nodos_fama):
        # No modificar
        for nodo in nodos_fama:
            self.insertar_nodo(nodo, self.raiz)

    def insertar_nodo(self, nuevo_nodo, padre=None):
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            siguiente_nodo = None
            if nuevo_nodo.usuario.fama >= padre.usuario.fama:
                siguiente_nodo = padre.hijo_derecho
            else:
                siguiente_nodo = padre.hijo_izquierdo

            if siguiente_nodo is None:
                if nuevo_nodo.usuario.fama >= padre.usuario.fama:
                    padre.hijo_derecho = nuevo_nodo
                else:
                    padre.hijo_izquierdo = nuevo_nodo
            else:
                self.insertar_nodo(nuevo_nodo, siguiente_nodo)

    def buscar_nodo(self, fama, padre=None):
        # El padre inicial no es la raiz :(
        if padre is None:
            padre = self.raiz
        if padre.usuario.fama == fama:
            return padre
        elif fama > padre.usuario.fama:
            siguiente = padre.hijo_derecho
        else:
            siguiente = padre.hijo_izquierdo
        if siguiente is None:
            return None
        else:
            return self.buscar_nodo(fama, siguiente)

    def print_arbol(self, nodo=None, nivel_indentacion=0):
        # No modificar
        indentacion = "|   " * nivel_indentacion
        if nodo is None:
            print("** DCCelebrity Arbol Binario**")
            self.print_arbol(self.raiz)
        else:
            print(f"{indentacion}{nodo.usuario.nombre}: "
                  f"{nodo.usuario.correo}:")
            if nodo.hijo_izquierdo:
                self.print_arbol(nodo.hijo_izquierdo,
                                 nivel_indentacion + 1)
            if nodo.hijo_derecho:
                self.print_arbol(nodo.hijo_derecho,
                                 nivel_indentacion + 1)
