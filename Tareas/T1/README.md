# Tarea 1: DCCapitolio :school_satchel:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 38 pts (27%)
##### ✅  Diagrama
##### ✅ Definición de clases, atributos y métodos
##### ✅ Relaciones entre clases
#### Simulaciones: 12 pts (8%)
##### ✅ Crear partida
#### Acciones: 43 pts (30%)
##### ✅ Tributo
##### ✅ Objeto
##### ✅ Ambiente
##### ✅ Arena
#### Consola: 34 pts (24%)
##### ✅ Menú inicio
##### ✅ Menú principal
##### ✅ Simular Hora
##### ✅ Robustez
#### Manejo de archivos: 15 pts (11%)
##### ✅ Archivos CSV
##### ✅ parametros.py
#### Bonus: 3 décimas máximo
##### ✅ Guardar Partida
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```ambientes.csv``` en ```./```
2. ```arenas.csv``` en ```./```
3. ```objetos.csv``` en ```./```
4. ```tributos.csv``` en ```./```
5. ```partida.txt``` en ```./```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```abc```: se usa la clase ```ABC``` y la decoración ```abstractmethod``` para crear clases virtuales.
2. ```copy```: se usa la función ```copy``` para crear copias de instancias para poder tener instancias inicialmente identicas pero que puedan ser modificad independientemente.
3.  ```datetime```: se usan las funciones ```now()``` y ```strftime()``` para obtener el dia y hora actual.
4. ```enum```: se usa la clase ```Enum``` para hacer más claro la transición de los menús en el código.
5. ```random```: se usan las funciones ```choice()```, ```sample()``` y ```random()``` para implementar el azar del juego.


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```archives```: Hecha para instanciar las clases de los tributos, objetos, etc, usando los datos de los archivos _csv_.
2. ```arena```: Contiene la clase ```Arena``` que representa una arena de los juegos y además administra la simulación del juego.
3. ```dccapitolio```: Contiene la clase ```DCCapitolio``` la cual administra los menús y las funciones para guardar la partida.
4. ```enums```: Contiene la clase ```Menu```, que hereda de la clase ```Enum```, que facilita y hace más legible la creación de menus en ```DCCapitolio```.
5. ```environment```: Contiene las clases ```Beach```, ```Mountain``` y ```Forest``` que heredan de la clase virtual ```Environment``` que representan los posible ambientes de una arena.
6. ```item```: Contiene las clases ```Consumable```, ```Weapon``` y ```SpecialItem``` que heredan de la clase virtual ```Item``` que representan los objetos que pueden tener los tributos.
8. ```parametros```: Contiene las constantes mencionadas en el enunciado, además, tiene los _paths_ de los archivos utilizados y una constante para modificar la cantidad de los participandes en un juego de DCCapitolio.
9. ```tribute```: Contiena la clase ```Tribute``` que representa un tributo y todas las propiedades y acciones que puedan tener.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para el número de encuentros en cada hora, se hiso que el número minimo de encuentros fuera 1 porque si se usaba solo la formula del enunciado causaba que el jugador tuviera una victoria asegurada una vez que un par de tributos murieran en las arenas más faciles.
2. Todos los archivos siguen el formato del enunciado correctamente.
    - Además, no se pueden usar ```,``` ni ```;``` en los archivos.
    - También se espera que los archivos _csv_ no cambien entren ejecuciones del programa ya que corrompen los datos de las partidas guardadas. En teoria aun podria usarse la partida guardada siempre y cuando ```environment.csv``` y ```objetos.csv``` tuvieran al menos las instancias utilizadas durante la partida.
3. Un máximo de un tributo por distrito se elije para los tributos utilizados como oponentes para seguir el _lore_ del programa más fielmente.
    - Aunque esto no se puede ver en el archivo ```tributos.csv``` de referencia ya que tiene un tributo por distrito.
    - Se pueden utilizar más distritos de los que estan en el archivo de referencia.
4. La cantidad total de partipantes en DCCapitolio se puede modificar usando la constante ```PARTICIPANT_NUMBER```, aunque se asume que debe que haber al menos esa cantidad de tributos con un distrito diferente cada uno (ver punto 3) en el archivo ```tributos.csv```.
5. Es posible que no hayan ganadores en DCCapitolio, esto puede pasar si un evento aleatorio elimina a todos los tributos vivos. Un mensaje correspondiente sale en la consola.
    - Naturalmente, el programa igual le anuncia al jugador que perdió.
6. Los metodos ```bakugan_mode``` y ```let_them_fight``` corresponden a las funciones para que un tributo se hiciera una _bolita_ y para simular los encuentros entre los tributos respectivamente.

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://stackoverflow.com/questions/181530/styling-multi-line-conditions-in-if-statements>: está implementado en el archivo ```arena.py``` en las líneas 69 y 70 y hace que los _if-statements_ puedan abarcar más de una linea para que no sea tan largo.
2. \<https://stackoverflow.com/questions/6470428/> está implementado en el archivo ```tribute.py``` en la linea 89 y hace que una sentencia ```except``` pueda capturar más de un tipo de ```Exception```.



## Descuentos
Por favor referirse al ```README.md``` de la _T0_.
