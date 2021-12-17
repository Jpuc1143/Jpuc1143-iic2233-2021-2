import requests


def info_api_curso(token):
    return requests.get(f"https://www.avanzada.ml/api/v2/bonus/ability?api_token={token}").json()

def enviar_test(token, test_id, respuesta):
    func_id = {
            1: "obtener_info_habilidad",
            2: "obtener_pokemones", 
            3: "obtener_pokemon_mas_alto",
            4: "obtener_pokemon_mas_rapido",
            5: "obtener_mejores_atacantes",
            6: "obtener_pokemones_por_tipo"
            }
    data = {
            "function_name": func_id[test_id],
            "function_response": respuesta
            }
    response = requests.post(f"https://www.avanzada.ml/api/v2/bonus/tests/{test_id}?api_token={token}", json={"test": data})
    print(response.json())
    return response.json()["result"] == "success"
