from collections import defaultdict
import requests


def obtener_info_habilidad(url):
    response = requests.get(url).json()
    result = {
            "name": response["name"],
            "effect_entries": list(filter(lambda x: x["language"]["name"] == "en", response["effect_entries"]))[0]["short_effect"],
            "pokemon": list(map(lambda x: {"name": x["pokemon"]["name"], "url": x["pokemon"]["url"]}, response["pokemon"]))
            }

    return result


def obtener_pokemones(pokemones):
    result = []
    for pokemon in pokemones:
        response = requests.get(pokemon["url"]).json()
        data = {
                "id": response["id"],
                "name": response["name"],
                "height": response["height"],
                "weight": response["weight"],
                "stats": dict(map(lambda x: (x["stat"]["name"] ,{"base_stat": x["base_stat"],"effort": x["effort"]}), response["stats"])),
                "types": list(map(lambda x: x["type"]["name"], response["types"]))
                }
        result.append(data)

    return result

def obtener_pokemon_mas_alto(pokemones):
    pass


def obtener_pokemon_mas_rapido(pokemones):
    pass


def obtener_mejores_atacantes(pokemones):
    pass


def obtener_pokemones_por_tipo(pokemones):
    pass
