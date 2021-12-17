import requests


def info_api_curso(token):
    return requests.get(f"https://www.avanzada.ml/api/v2/bonus/ability?api_token={token}").json()

def enviar_test(token, test_id, respuesta):
    pass
