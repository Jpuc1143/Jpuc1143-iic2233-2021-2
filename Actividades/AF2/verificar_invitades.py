def verificar_edad(invitade):
    if invitade.edad < 0:
        raise ValueError(f"Error: la edad de {invitade.nombre} es negativa")


def corregir_edad(invitade):
    try:
        verificar_edad(invitade)
    except ValueError:
        invitade.edad *= -1
        print(f"El error en la edad de {invitade.nombre} ha sido corregido")


def verificar_pase_movilidad(invitade):
    if not isinstance(invitade.pase_movilidad, bool):
        raise TypeError(f"Error: el pase de movilidad de {invitade.nombre} no es un bool")


def corregir_pase_movilidad(invitade):
    try:
        verificar_pase_movilidad(invitade)
    except TypeError:
        invitade.pase_movilidad = True
        print(f"El error en el pase de movilidad de {invitade.nombre} ha sido corregido")


def verificar_mail(invitade):
    # Se asume que el correo solo tiene 1 @ y que termina con '.cl'
    split = invitade.mail[0:-4].split("@")
    domain = split[1]

    if domain != "uc":
        raise ValueError(f"Error: El mail de {invitade.nombre} no está en el formato correcto")


def corregir_mail(invitade):
    try:
        verificar_mail(invitade)
    except ValueError:
        split = invitade.mail[0:-4].split("@")
        user = split[1]
        domain = split[0]

        invitade.mail = user + "@" + domain + ".cl"
        print(f"El error en el mail de {invitade.nombre} ha sido corregido")


def dar_alerta_colado(nombre_asistente, diccionario_invitades):
    try:
        asistente = diccionario_invitades[nombre_asistente]
        print(f"{asistente.nombre} esta en la lista y tiene edad {asistente.edad}")
    except KeyError:
        print(f"Error: {nombre_asistente} se está intentando colar al carrete")
