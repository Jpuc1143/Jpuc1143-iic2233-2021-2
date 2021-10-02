from dccapitolio import DCCapitolio


def anti_globals_function():
    # ¯\_(ツ)_/¯
    capitolio = DCCapitolio()
    capitolio.main_loop()
    print("Gracias por honrar al capitolio!")
    # Posible alternativa: hacer que el constructor tenga el main loop, y no asignar la instancia a
    # una variable para evitar la global(?)


if __name__ == "__main__":
    anti_globals_function()
