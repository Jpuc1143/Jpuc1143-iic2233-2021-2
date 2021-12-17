from collections import defaultdict
import requests
from functools import reduce


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
                "stats": dict(map(lambda x: (x["stat"]["name"], {"base_stat": x["base_stat"],"effort": x["effort"]}), response["stats"])),
                "types": list(map(lambda x: x["type"]["name"], response["types"]))
                }
        result.append(data)

    return result

def obtener_pokemon_mas_alto(pokemones):
    return max(pokemones, key=lambda x: x["height"])["name"]


def obtener_pokemon_mas_rapido(pokemones):
    return max(pokemones, key=lambda x: x["stats"].get("speed", {"base_stat": 0})["base_stat"])["name"]


def obtener_mejores_atacantes(pokemones):
    result = list(map(lambda x: x["name"], sorted(filter(lambda x: "attack" in x["stats"] and "defense" in x["stats"], pokemones), key=lambda x: x["stats"]["attack"]["base_stat"]/x["stats"]["defense"]["base_stat"], reverse=True)))
    return result[:min(5, len(result))]


def obtener_pokemones_por_tipo(pokemones):
    # return reduce(lambda x, y: tuple(map(lambda z: x[z] += y["name"], y["types"])), pokemones, defaultdict(list))
    result = defaultdict(list)
    for pokemon in pokemones:
        tuple(map(lambda x: result[x].append(pokemon["name"]), pokemon["types"]))

    return result
