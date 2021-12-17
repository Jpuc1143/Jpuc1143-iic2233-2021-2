from pokemon import (obtener_info_habilidad, obtener_pokemones,
                     obtener_pokemon_mas_alto, obtener_pokemon_mas_rapido,
                     obtener_mejores_atacantes, obtener_pokemones_por_tipo)
from api_curso import info_api_curso, enviar_test


token = "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2VtYWlsIjoiamFpbWUucGVyZXpAdWMuY2wifQ.SVhiW_TbcjCRaFPl_HdW4ncslIk3u90tGfkes4xpuv0"  # Ingresar tu API Token personal aquí

info_curso = info_api_curso(token)

if not info_curso:
    print("No se pudo obtener la información de la API del curso")
    exit()

url = info_curso["ability"]["url"]
info_habilidad = obtener_info_habilidad(url)
pokemones = obtener_pokemones(info_habilidad["pokemon"])

mas_alto = obtener_pokemon_mas_alto(pokemones)
mas_rapido = obtener_pokemon_mas_rapido(pokemones)
mejores_atacantes = obtener_mejores_atacantes(pokemones)
pokemones_por_tipo = obtener_pokemones_por_tipo(pokemones)

print("Mas alto", mas_alto)
print("Mas rapido", mas_rapido)
print("Mejores atacantes", mejores_atacantes)
print("Pokemones por tipo", pokemones_por_tipo)

print(enviar_test(token, 1, info_habilidad),
enviar_test(token, 2, pokemones),
enviar_test(token, 3, mas_alto),
enviar_test(token, 4, mas_rapido),
enviar_test(token, 5, mejores_atacantes),
enviar_test(token, 6, pokemones_por_tipo))
