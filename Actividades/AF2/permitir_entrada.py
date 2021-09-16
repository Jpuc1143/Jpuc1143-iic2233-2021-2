from excepciones_covid import RiesgoCovid


# NO DEBES MODIFICAR ESTA FUNCIÓN
def verificar_sintomas(invitade):
    if invitade.temperatura > 37.5:
        raise RiesgoCovid("fiebre", invitade.nombre)
    elif invitade.tos:
        raise RiesgoCovid("tos", invitade.nombre)
    elif invitade.dolor_cabeza:
        raise RiesgoCovid("dolor_cabeza", invitade.nombre)


def entregar_invitados(diccionario_invitades):
    lista_final = []
    for nombre, invitade in diccionario_invitades.items():
        try:
            verificar_sintomas(invitade)
            lista_final.append(nombre)
        except RiesgoCovid as err:
            err.alerta_de_covid()

    return lista_final
