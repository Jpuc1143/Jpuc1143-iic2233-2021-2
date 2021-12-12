# Tarea 3: DCCalamar :school_satchel:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 23 pts (18%)
##### ✅ Protocolo
##### ✅ Correcto uso de sockets
##### ✅ Conexión
##### ✅ Manejo de clientes
#### Arquitectura Cliente - Servidor: 31 pts (24%)
##### ✅ Roles <explicacion\>
##### ✅ Consistencia <explicacion\>
##### ✅ Logs <explicacion\>
#### Manejo de Bytes: 20 pts (15%)
##### ✅ Codificación
##### ✅ Decodificación
##### ✅ Encriptación
##### ✅ Integración
#### Interfaz gráfica: 31 pts (24%)
##### ✅ Modelación <explicacion\>
##### ✅ Ventana inicio <explicacion\>
##### ✅ Sala Principal <explicacion\>
##### 🟠 Ventana de Invitación: No se puede retar a los jugadores que esten invitado, sin embargo no vuelven a estar disponibles al rechazar la invitación.
##### 🟠 Sala de juego: las rondas funcionan aunque no avisan los resultados y se deben que inferir de los datos del juego.
##### ✅ Ventana final
#### Reglas de DCCalamar: 21 pts (16%)
##### ✅ Inicio del juego
##### ✅ Ronda
##### ✅ Termino del juego
#### General: 4 pts (3%)
##### ✅ Parámetros (JSON) <explicacion\>
#### Bonus: 5 décimas máximo
##### ❌ Cheatcode
##### ✅ Turnos con tiempo
## Ejecución :computer:
El módulo principal del cliente de la tarea a ejecutar es  ```cliente/main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```parametros.json``` en ```cliente```
2. ```Sprites``` en ```cliente```
3. ```Avatares``` en ```cliente/Sprites```
4. ```Decoraciones``` en ```cliente/Sprites```
5. ```Juego``` en ```cliente/Sprites```
6. ```Logos``` en ```cliente/Sprites```

El módulo principal para el servidor de la tarea a ejecutar es ```servidor/main.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```parametros.json``` en ```servidor```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```librería_1```: ```función() / módulo```
2. ```librería_2```: ```función() / módulo``` (debe instalarse)
3. ```PyQt5```: Para la creación de los aspectos visuales del programa.
4. ```threading```:
    * ```Thread```: ejecutar varios hilos al mismo tiempo en el cliente y el servidor.
    * ```Condition```: sincronizar la creación y obtención de datos entre los hilos.
    * ```excepthook`: interceptar excepciones para mostrarlas en un _pop-up_ modal en el cliente.
5. ```abc```: para la creacion de la clase virtual ```DCConnection```. No muy utilizada porque basicamente todo sus metodos fueron _overriden_ en sus subclases.
6. ```json```: ```loads``` y ```dumps``` para enviar comandos entre el servidor y el cliente. También ```load``` para leer los parametros del ```parametros.json``` correspondiente.
7. ```sys```:  ```excepthook``` para interceptar excepciones para mostrarlas en un _pop-up_ modal en el cliente.
8. ```os```: ```path.join``` para crear _paths_ independientes de la plataforma.
9. ```random```: ```shuffle``` para la elección aleatoria de avatares y de quien empieza primero en las partidas.
10. ```re```: ```fullmatch``` para verificar la validez de la fecha de nacimiento.
11. ```socket```: para toda la comunicación entre cliente y servidor.

### Librerías propias
Por otro lado, los módulos que fueron creados para tanto el cliente como el servidor son (_hardlinks_ fueron los __MVP__ de esta sección):

1. ```dcconnection```: ```DCConnection``` se encarga de todo sobre la comunicación encriptrada entre cliente y servidor. Notablemente esta el metodo ```do_command``` que es modificado en las subclases del cliente y servidor para darle las funciones a los comandos enviados.
3. ```parameters```: La clase ```Parameters``` lee de ```parametros.json``` para otorgar acceso a las constantes de los programas con una interfaz similar a la de ```parametros.py``` de tareas anteriores.

Adicionalmente, los siguientes archivos son para el renderizado y la lógica de las ventanas utilizadas en el cliente; donde __X__ representa ```window``` o ```logic``` para el código de _frontend_ y _backend_ respectivamente:
1. ```start_X```: la ventana de _login_ del cliente.
2. ```main_X```: la ventana con la sala de espera. Las invitaciones se hacen a travez de _pop-ups_. Mientras se este en la sala de espera, el _backend_ continuamente pide los datos de la sala de espera sin interrumpir la interfaz.
3. ```game_X```: la ventana donde se realiza el juego. El _backend_ es un _wrapper_ glorificado que obtiene la simulación del juego del servidor.
4. ```end_X```: la ventana que muestra los resultados al terminar el juego.
5. ```client_connection```: subclase de ```DCConnection``` que administra los comandos enviados y recibidos por el servidor.
    * ```send_command_signal``` es un función similar a ```send_command``` de ```DCConnection```. Al igual que ella se envia un comando, pero al recibir una respuesta, se hace un ```emit()``` a la señal dada como parametro usando el valor retornado por el servidor como argumento.
6. ```endpoint_error```:
    * ```EndpointError```: hereda de ```Exception``` para representar cualquier error recibido del servidor. Al ser capturado por ```sys.excepthook``` muestra un _pop-up_ y __no para__ la ejecución del cliente.
    * ```FatalEndpointError```: hereda de ```EndpointError```, pero para la ejecución del programa al ser capturado.

Finalmente, los siguientes módulos son para el uso exclusivo del seridor:
1.```dccalamar```: administra los datos de los usuarios (representados por la clase ```User```), invitaciones y juegos que se realizan en el servidor. ```MarbleGame``` es una subclase de ```Thread``` y procesa un juego del servidor y sincroniza los cliente participantes.
2. ```server_connection```: subclase de ```DCConnection``` con función similar al modulo encontrado en el cliente. A diferencia de ```client_connection```, las excepciones son atrapadas en la función ```run()``` de ```ServerConnection``` y terminan la conexión y hacen _log-out_ al usuario correspondiente.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Aunque el diseño de ```DCConnection``` permite que el programa pueda ser utilizado en situaciones de alta latencia, no se ha probado extensamente y se asume que no va a ser parte de la correción.
2. El enunciado menciona que solo pueden estar hasta cuatro personas en la sala de espera. El servidor solo aceptara que cuatro usuarios esten hecho _log-in_ al mismo tiempo. Sin embargo, esto puede ser modificado con la constante del servidor ```MAX_USERS``` que puede aumentarse sin problemas ya que el cliente tiene un _widget_ con _scroll_ para mostrar los usuarios disponibles. 
3. Para el bonus de turnos con tiempo, se usa la constante del servidor ```TIEMPO_TURNO``` para ajustar el tiempo de los turnos. La duración es de 10 segundos por defecto. Adicionalmente, si ambos jugadores no hacen apuestas en su turno, el jugador que empieza primero gana por defecto.
4. Salir de un juego en progreso no causa que el contrincante salga del juego inmediatamente; el contrincante va a la ventana de resultados una vez haga su propia apuesta. El ganador se registra inmediatamente en el servidor asi que no hay problemas si el contrincante se desconecta antes de hacer su apuesta.


-------



## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://stackoverflow.com/questions/46301811/gitignore-all-files-in-folders-but-keep-folder-structure>: este hace que ```.gitignore``` mantenga la estructura de la carpeta ```Sprites``` aunque no tenga ningun archivo _tracked_ en ella.
2. \<https://stackoverflow.com/questions/21586643/pyqt-widget-connect-and-disconnect>: este código hace que se pueda desconectar todas las señales de un _slot_ y esta implementado entre las lineas 21 y 26 de ```cliente/client_connection.py```
3. \<https://stackoverflow.com/questions/3155436/getattr-for-static-class-variables-in-python> : este código hace que se pueda usar ```__getattr__``` estaticamente y es implementado en ```parameters.py```




## Descuentos
Por favor referirse al ```README.md``` de la _T2_.
