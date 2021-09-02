from mascota import Perro, Gato, Conejo


def cargar_mascotas(archivo_mascotas):
    lista_mascotas = []
    file = open(archivo_mascotas, "r")
    
    file.readline()
    for line in file:
        mascota = line.strip().split(",")
        mascota[4] = int(mascota[4])
        mascota[5] = int(mascota[5])
        lista_mascotas.append(mascota)

    file.close()
    return lista_mascotas
