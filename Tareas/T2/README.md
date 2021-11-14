# Tarea 2: DCCrossy Frog :school_satchel:

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Ventana de Inicio: 4 pts (3%)
##### ✅ Ventana de Inicio
#### Ventana de Ranking: 5 pts (4%)
##### ✅ Ventana de Ranking
#### Ventana de juego: 13 pts (11%)
##### ✅ Ventana de juego
#### Ventana de post-nivel: 5 pts (4%)
##### ✅ Ventana post-nivel
#### Mecánicas de juego: 69 pts (58%)
##### ✅ Personaje
##### ✅ Mapa y Áreas de juego
##### ✅ Objetos
##### ✅ Fin de Nivel
##### ✅ Fin del juego
#### Cheatcodes: 8 pts (7%)
##### ✅ Pausa <explicacion\>
##### ✅ V + I + D
##### ✅ N + I + V
#### General: 14 pts (12%)
##### ✅ Modularización
##### ✅ Modelación
##### ✅ Archivos
##### ✅ Parametros.py
#### Bonus: 10 décimas máximo
##### ❌ Ventana de Tienda
##### ❌ Música 
+ Lo tenia casi listo, pero tuve problemas de audio y no pude probarlo para hacerle commit 😭
##### ✅ Checkpoint 
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```puntaje.txt``` en ```./```. Sin embargo, el programa automaticamente lo crea si no existiera.
2. ```sprites``` en ```./```
3. ```Objetos``` en ```sprites```
4. ```Mapa``` en ```sprites```
5. ```Personajes``` en ```sprites```
6. ```Logo.png``` en ```sprites```
7. ```Verde``` en ```sprites/Personajes```. En esta carpeta estan las _sprites_ de la rana controlada por el jugador.
En las carpetas anteriores deben estar presentes las _sprites_ que van a ser utilizadas por las ```Entities``` del programa.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:
1. ```PyQt5```: Para la creación de los aspectos visuales del programa.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:
1. ```parametros.py```: Contiene las constantes del enunciado, los _paths_ de las imagenes usadas y cualquier otra constante utilizada como el tamaño y velocidad de los autos.
2. ```entity```: La clase ```entity``` es la base para todas las clases que representen un objeto en el juego. Todas las clases que hereden de ella, como ```Frog``` y ```Item```, tambien están presentes.
3. ```keyboard_status```: La clase de utilidad ```KeyboardStatus``` se utiliza para determinar si una tecla esta siendo presionada o no ya que _QT_ solo dice cuando las teclas son presionadas y soltadas.

Adicionalmente, los siguientes archivos son para el renderizado y la lógica de las ventanas utilizadas; donde __X__ representa ```window``` o ```logic``` para el código de _frontend_ y _backend_ respectivamente:
1. ```X_start```: La ventana de inicio.
2. ```X_ranking```: La ventana de puntuaciones. También se ordenan las puntuaciones en el _backend_
3. ```X_game```: La ventana que contiene el juego y la barra de estadisticas del jugador. El _backend_ simula todas las acciones del juego.
4. ```X_post_game```: La ventana que muestra los resultados del juego. También se puede usar para ir al siguiente nivel si no se ha perdido aun. Las puntuaciones son guardas al archivo de ```puntaje.txt``` en el _backend_


## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. La tecla de salto fue cambiada a "J". Esto es necesario porque la barra de espacio apreta un ```QPushButton``` al usarse. Utilizar ```setFocus()``` en el _widget_ del juego no funciona ya que causa que no se puedan apretar los botones.
2. Se determina si la rana esta o no tocando el agua o un tronco usando solo su punto central. Por ello es que la rana puede estar tocando el agua parcialmente.
3. Las teclas para los _cheatcodes_ se tienen que apretar al mismo tiempo para funcionar.


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://github.com/IIC2233/contenidos/blob/main/semana-07/1-interfaces-gr%C3%A1ficas.ipynb>: esto hace un print del _traceback_ cuando hay un error y está implementado en el archivo ```main.py``` en las líneas 17 a la 20.



## Descuentos
Por favor referirse al ```README.md``` de la _T1_.
