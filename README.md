# info de la materia: STxxxx <nombre>
# Estudiante(s): Humberto Antonio Carbonó, David Elias Franco Velez - hacarbonop@eafit.edu.co, defrancov@eafit.edu.co
# Profesor: Alvaro Enrique Ospina, aeospinas@eafit.edu.co
# Arquitectura P2P y Comunicación entre procesos mediante API REST, RPC y MOM
# 1. Breve descripción de la actividad

Este código implementa un sistema distribuido de compartición de archivos entre pares (peers) utilizando Flask como marco para las APIs REST. En este sistema, múltiples nodos (o peers) pueden registrarse con un nodo central (superpeer), y luego pueden compartir y buscar archivos entre ellos.
## Componentes principales
### Superpeer
Es el encargado de registrar los peers que se conectan a la red, además mantiene un registro de los archivos que cada peer tiene disponible y notifica a los peers sobre la existencia de otros peers en la red.
### Peer
Cada peer tiene un directorio local de archivos que comparte en la red. Los peers pueden buscar archivos en su propio directorio y en el de otros peers conectados. Estos se registran con el superpeer y obtienen la lista de otros peers y sus archivos para postriormente poder descargar archivos de otros peers si el archivo no se encuentra en su directorio local.

### Flujo básico
1. Un peer se registra con el superpeer enviando su dirección y lista de archivos.
2. El superpeer distribuye la información del nuevo peer a los demás peers ya registrados.

3. Un peer puede buscar un archivo en su directorio local o en el de otros peers a través de la red.
4. Si el archivo se encuentra en otro peer, se puede descargar utilizando el endpoint correspondiente.
5. Los peers actualizan la información de los otros peers cuando se registran nuevos nodos en la red, permitiendo que la red se mantenga dinámica y actualizada.

## 1.1. ¿Qué aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

### Requerimientos Funcionales
- Se ha desarrollado un sistema Peer-to-Peer (P2P) donde los peers (nodos) pueden interactuar entre sí para compartir archivos. El sistema incluye un peer especial denominado "superpeer" (register.py) que gestiona el registro y la distribución de información sobre los peers en la red.
- Se ha implementado la funcionalidad para que los peers se registren en el superpeer mediante un endpoint '<b>/register_peer</b>'. Este registro incluye el envío de la dirección del peer y la lista de archivos locales que están disponibles para compartir.
- El superpeer mantiene un registro de todos los nodos y sus archivos, y distribuye esta información a todos los demás nodos registrados para que cada uno tenga un mapa actualizado de los archivos disponibles en la red.
- Los peers pueden buscar archivos en su propia lista de archivos locales, así como en la lista de archivos de los peers vecinos que han registrado en el superpeer. Si el archivo no está disponible localmente, el peer consulta a sus vecinos para encontrar y descargar el archivo solicitado mediante el endpoint <b>/search_file</b>.
- Cada vez que un nuevo nodo se registra en la red, se notifica a los demas nodos mediante el endpoint '<b>update_neighbors</b>' actualizando la lista de archivos compartidos por cada peer
- Se implementó la gestión de errores en las solicitudes HTTP entre nodos, manejando situaciones en las que un nodo no responde o no se puede contactar, y asegurando que estas fallas no afecten el funcionamiento global del sistema.

### Requerimientos no Funcionales

- El sistema se diseñó para minimizar la latencia y optimizar la comunicación entre peers, utilizando peticiones HTTP directas y estructuras de datos eficientes para la gestión de archivos y peers.

- El código se ha organizado en funciones y rutas claramente definidas, lo que facilita la extensión y mantenimiento del sistema. La separación del superpeer y los peers en diferentes scripts también contribuye a la modularidad del sistema.

## 1.2. ¿Qué aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor? (requerimientos funcionales y no funcionales)
El servicio no se desplegó dado que no se consideró necesario para el alcance del reto. Además, debido a limitaciones de tiempo, se priorizaron otros aspectos del proyecto que eran más críticos para cumplir con los objetivos principales de la actividad.

La implementación se está llevando a cabo de manera local, lo que permite realizar pruebas y ajustes en un entorno controlado sin la necesidad de desplegar el servicio en un servidor remoto. 

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

## Arquitectura

<img src='./Arquitectura p2p.png'></img>

El sistema sigue una arquitectura Peer-to-Peer (P2P) con un superpeer central que gestiona el registro de peers y distribuye información. Los peers normales se registran en el superpeer, comparten archivos, y pueden buscar y descargar archivos de otros peers.

## Patrones de Diseño

Usamos los siguientes patrones:

### Cliente Servidor
Los peers actúan tanto como clientes, como servidores. Mientras que el superpeer gestiona la red.
### P2P
Los peers se comunican directamente entre sí para compartir archivos, utilizando el superpeer solo para la configuración inicial.
### Patron Observador
El superpeer notifica a los peers sobre nuevos registros y actualizaciones, similar al patrón de observador.

## Buenas Practicas Utilizadas
- El código tuvo una separacion en módulos claros para el superpeer y los peers, facilitando el mantenimiento.

- Implementamos un manejo robusto de errores en la comunicación entre peers para asegurar la estabilidad del sistema.

- Hicimos uso de un archivo .config para configurar parámetros clave, permitiendo flexibilidad y facilidad de uso.


# 3. Descripción del ambiente de desarrollo, técnico y de ejecución: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## Lenguaje de Programacion
Python3
### Librerias y Paquetes
Flask (2.0.1)
Requests(2.25.1)
ConfigParser(5.0.2)
Argparse(1.1)

## Entorno de Desarrollo

### Sistema Operativo
Windows 11 (Es posible hacer uso de la misma manera en todos los sitemas operativos)

### Entorno de Desarrollo
Python 3.12.3
pip 24.2

## Datos Adicionales
Para instalar los paquetes requeridos en esta entrega se tiene que ejecutar el siguiente comando

```
pip install flask==2.0.1 requests==2.25.1 configparser==5.0.2
```


## como se compila y ejecuta.

Para compilar y ejecutar este codigo hay dos pasos sobre todo que hay que hacer, el primero es con respecto a la ejecucion de register.py, que es el archivo que nos va a permitir registrar a todos los peers dentro de la red, se hace de la siguiente manera, y varia el comando inicial de acuerdo a la respectiva instalacion de python en las computadoras.

```
py register.py
```

y para la ejecucion de los peers, que pueden ser cuantos peers se desee, el comando en consola es de la siguiente manera

```
py peer.py peerx.config
```
<b>IMPORTANTE</b>
<br>
Si se desean crear más peers es necesario duplicar los archivos de configuración que está con el proyecto, por ejemplo, si se desea crear un peer 4, entonces se crea el archivo peer4.config con las mismas instrucciones de los otros peerx.config pero cambiándole el puerto.

## detalles del desarrollo.
El desarrollo se centró en implementar un sistema P2P básico utilizando un superpeer para facilitar el registro y la sincronización de peers, lo que permitió mantener un control centralizado mientras los peers compartían y buscaban archivos en sus directorios locales. Cada peer se configuró dinámicamente mediante un archivo .config, y la comunicación se manejó a través de API REST usando Flask. Se realizaron pruebas locales para validar la funcionalidad de registro, búsqueda, y actualización de vecinos, priorizando la simplicidad y eficiencia en la gestión de la red. 

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
Este proyecto utiliza un enfoque modular donde los parámetros clave, como la IP, puertos, directorios de archivos, y la conexión al superpeer, se configuran a través de un archivo de configuración .config.

    El archivo .config es el principal mecanismo para configurar los parámetros del sistema. Este archivo es leído al iniciar el proceso del peer y contiene la siguiente información clave: IP de listening, puerto, directorio de archivos locales y dirección IP del superpeer.

## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## opcionalmente - si quiere mostrar resultados o pantallazos 

# IP o nombres de dominio en nube o en la máquina servidor.

Este proyecto no se desplego, por lo que para ejecutarlo se debe hacer en la terminal.

# referencias:

"Designing Data-Intensive Applications" by Martin Kleppmann
<br>
"Peer-to-Peer: Harnessing the Power of Disruptive Technologies" by Andy Oram (Editor)
<br>
https://docs.python.org/3/
<br>
https://flask.palletsprojects.com/en/3.0.x/
