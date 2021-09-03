# Tarea 0: DCCommerce :school_satchel:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Menú de Inicio (14pts) (14%)
##### ✅ Requisitos
##### ✅ Iniciar sesión
##### ✅ Ingresar como usuario anónimo
##### ✅ Registrar usuario
##### ✅ Salir
#### Flujo del programa (35pts) (35%) 
##### ✅ Menú Principal
##### ✅ Menú Publicaciones
##### ✅ Menú Publicaciones Realizadas
#### Entidades 15pts (15%)
##### ✅ Usuarios
##### ✅ Publicaciones
##### ✅ Comentarios
#### Archivos: 15 pts (15%)
##### ✅ Manejo de Archivos
#### General: 21 pts (21%)
##### ✅ Menús
##### ✅ Parámetros
##### ✅ Módulos
##### ✅ PEP8
## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```publicaciones.csv``` en ```./```
2. ```usuarios.csv``` en ```./```
3. ```comentarios.csv``` en ```./```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```datetime```: se usan las funciones ```now()``` y ```strftime()``` para obtener el dia y hora actual.
2. ```enum```: se usa la clase ```Enum``` para hacer más claro la transición de los menús en el código.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```csv_utils```: Contiene a ```read_csv``` y ```write_csv``` para la transormación entre los datos _csv_ y las estructuras de _Python_.
2. ```user_actions```: Hecha para hacer modular las acciones de los usuarios como publicar comentarios, registrarse o borrar publicaciones.
3. ```parametros```: Además de las constantes mencionadas en el enunciado, contiene un _Enum_ para facilitar la lectura del código.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. El contenido de todos los csv siempre va a estar bien formateados.
2. El log-in de los usuarios se rige con un codigo de honor y no necesita contraseña. 
3. Los archivos csv son una abstracción de la conexión entre la aplicación y los servidores de DCCommerce.

Consideraciones adicionales:

1. El programa no está diseñado para una cantidad gigante de publicaciones o comentarios, ya que, se muestran todas las publicaciones al mismo tiempo y se escriben todos los datos de nuevo a los _csv_ cuando hay un cambio.
2. Debido al uso de archivos _csv_ en vez de un _DBMS_, se hicieron unas decisiones de diseño... _"interesantes"_... para la creación del programa.


-------


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. <https://stackoverflow.com/a/40003478>: este está implementado en el archivo ```main.py``` en las líneas 3 a la 7 y hace que la sentencia ```import``` sea multi-linea y este más organizada
2. <https://docs.python.org/3/library/enum.html?highlight=enum>: este está implementado en el archivo ```parametros.py``` en las líneas 10 a la 23 y hace que la los estados de los menus tengan un nombre textual en vez de ser número para que sean m


## Descuentos
Por favor no.
