
def cargar_datos(path):
    ayudantes = []
    file = open(path)
    for line in file:
        ayudantes.append(line.strip().split(","))
    file.close()
    return ayudantes



# Completa esta funcion para encontrar la informacion del ayudante entregado
def buscar_info_ayudante(nombre_ayudante, lista_ayudantes):
    ayudantes = {x[0].lower(): x for x in lista_ayudantes}

    if nombre_ayudante.lower() in ayudantes:
        data = ayudantes[nombre_ayudante.lower()]
        data[0] = nombre_ayudante
        return data
    else:
        return None


# Completa esta funcion para que los ayudnates puedan saludar
def saludar_ayudante(info_ayudante):
    return "Hola " + info_ayudante[0] + " tu informacion es " + info_ayudante[1] + ", " + info_ayudante[2] + ", " + info_ayudante[3]

if __name__ == '__main__':
    print(saludar_ayudante(buscar_info_ayudante("triNi balart",cargar_datos("ayudantes.csv"))))

