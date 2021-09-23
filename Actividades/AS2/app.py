from random import randint
from time import sleep
from pedido import Pedido
from shopper import Shopper
from threading import Thread


class DCComidApp(Thread):

    def __init__(self, shoppers, tiendas, pedidos):
        # NO MODIFICAR
        super().__init__()
        self.shoppers = shoppers
        self.pedidos = pedidos
        self.tiendas = tiendas

    def obtener_shopper(self):
        while True:
            for shopper in self.shoppers:
                if not shopper.ocupado:
                    return shopper

            print("Todos los Shoppers estan ocupados. Esperando...")
            Shopper.evento_disponible.wait()
            print("Un shopper se ha desocupado")
            Shopper.evento_disponible.clear()

    def run(self):
        for item in pedidos:
            pedido = Pedido(item[0], item[1], item[2])
            shopper = self.obtener_shopper()
            shopper.asignar_pedido(pedido)
            self.tienda.ingresar_pedido(pedido)
            sleep.randint(1, 5)


if __name__ == '__main__':
    pass
