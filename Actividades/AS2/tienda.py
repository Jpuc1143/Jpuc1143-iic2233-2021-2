from threading import Thread, Lock
from time import sleep
from random import randint


class Tienda(Thread):
    def __init__(self, nombre):
        # NO MODIFICAR
        super().__init__()
        self.nombre = nombre
        self.cola_pedidos = []
        self.abierta = True

        # COMPLETAR DESDE AQUI
        self.lock = Lock()


    def ingresar_pedido(self, pedido, shopper):
        with self.lock:
            self.cola_pedidos.append((pedido, shopper))

    def preparar_pedido(self, pedido):
        delay = randint(1, 10)
        print(f"{self.nombre} cocinara durante {delay} segundos")
        sleep(delay)
        print(f"{self.nombre} termino de preparar el pedido")

    def run(self):
        while self.abierta:
            self.lock.acquire()
            if len(self.cola_pedidos) > 0:
               pedido = self.cola_pedidos.pop(0)
               self.lock.release()

               self.preparar_pedido(pedido)
               pedido.evento_pedido_listo.set()
               pedido.evento_llego_repartidor.wait()
               print(f"Pedido {pedido.id} ha sido retirado")

            else:
                self.lock.release()
                delay = randint(1, 5)
                print(f"{self.nombre} se esta tomando un descanso de {delay} segundos")
                sleep(delay)
