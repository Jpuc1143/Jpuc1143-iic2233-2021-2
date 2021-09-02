from mascota import Perro, Gato, Conejo


def cargar_mascotas(archivo_mascotas):
    lista_mascotas = []
    file = open(archivo_mascotas, "r")

    file.readline()
    for line in file:
        mascota = line.strip().split(",")
        
        if mascota[1] == "perro":
            entidad = Perro(mascota[0],mascota[2],mascota[3],int(mascota[4]),int(mascota[5]))

        elif mascota[1] == "gato":
            entidad = Gato(mascota[0],mascota[2],mascota[3],int(mascota[4]),int(mascota[5]))

        elif mascota[1] == "conejo":
            entidad = Conejo(mascota[0],mascota[2],mascota[3],int(mascota[4]),int(mascota[5]))
        
        lista_mascotas.append(entidad)
        
    file.close()
    return lista_mascotas
