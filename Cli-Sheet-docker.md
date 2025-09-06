
# CLI Sheet de comandos Docker más usados


## Gestión de Imágenes


- **docker pull**: Descarga una imagen desde Docker Hub o una imagen local.

```bash
docker pull python:3.11-alpine
```
*Después de **:3.11-alpine** seleccionamos el tag o la versión de la imagen que descargamos.*


- **docker images**: Lista todas las imágenes descargadas en el sistema.

```bash
docker images
```


- **docker rmi**: Elimina una imagen por su nombre o ID.

```bash
docker rmi hello-world
# o por ID
docker rmi 7c838239047vs
```


- **docker build**: Construye una imagen a partir de un Dockerfile.

```bash
docker build -t mi-app-web .
```
*La bandera **-t (tag)** sirve para asignar a la imagen un nombre y una versión, para facilitar su organización y control de versiones.*


## Gestión de Contenedores


- **docker run**: Crea y ejecuta un nuevo contenedor a partir de una imagen.

```bash
docker run -d --name mi-contenedor-nginx -p 8080:80 nginx
```
*La bandera **-d (detach)** sirve para ejecutar el contenedor en segundo plano, permitiendo seguir usando el terminal host. Ideal para lanzar contenedores activos como un servidor web o BBDD.*
*La bandera **--name** es para darle un nombre al contenedor.*
*La bandera **-p (publicar)** se utiliza para publicar los puertos del contenedor a la máquina local, permitiendo que el exterior se comunique con el contenedor y su servicio.*
  

- **docker ps**: Lista los contenedores en ejecución.

```bash
docker ps -a
```
*La bandera **-a (all)** sirve para mostrar todos los contenedores que existen en el sistema.*


- **docker start**: Inicia un contenedor.

```bash
docker start mi-contenedor
```


- **docker stop**: Detiene un contenedor.

```bash
docker stop mi-contenedor
```


- **docker restart**: Reinicia un contenedor.

```bash
docker restart mi-contenedor
```


- **docker exec**: Ejecuta un comando dentro de un contenedor en ejecución o permite acceder a la terminal del contenedor con ciertas banderas.

```bash
docker exec -it mi-contenedor bash
```
*La bandera **-i (interactivo)** mantiene abierta la entrada de comandos al terminal del contenedor. Sin esta bandera, una vez termine el comando, el contenedor se detendría.*
*La bandera **-t (terminal)** permite acceder al terminal del contenedor y escribir comandos como si fuera el terminal de la propia máquina.*


- **docker logs**: Muestra la salida del contenedor, es decir, los mensajes de error e información. Perfecto para buscar información o tener un registro de cómo está funcionando el contenedor.

```bash
docker logs mi-contenedor
# o por ID
docker logs <ID>
```


- **docker rm**: Elimina un contenedor por su nombre o ID.

```bash
docker rm mi-contenedor
# o por ID
docker rm <ID>
```


## Gestión de Volúmenes y Redes


- **docker volume create**: Crea un volumen para persistir datos.

```bash
docker volume create datos-mysql
```
*En este caso, `datos-mysql` es el nombre del volumen que se guardará en una carpeta oculta `/var/lib/docker/volumes/`. Con los volúmenes podemos hacer que dos contenedores los compartan y los datos no se pierdan si se apaga el contenedor.*

*Para compartir dos contenedores que tengan el mismo volumen:*

Primer contenedor:
```bash
docker run -d --name mysql-1 \
  -v datos-mysql:/app/data \
  mysql:3.9-alpine
```
Segundo contenedor:
```bash
docker run -d --name nginx-2 \
  -v datos-mysql:/app/data \
  nginx:3.9-alpine
```
*Como podemos ver, los dos contenedores distintos tendrán el mismo volumen, con el que se guardarán los datos y estarán compartidos entre ellos.*


- **docker -v "rutalocal:rutacontenedor"**: Es una manera de pasarle el volumen de un directorio local de tu máquina host si estás trabajando en un proyecto en local y quieres hacer cambios en el momento. Bastante útil si estás desarrollando y lanzas un servidor web como contenedor.

```bash
docker run -d --name mysql \
  -v /Users/Documents/bbdd:/app/data
```


- **docker volume ls**: Lista todos los volúmenes.

```bash
docker volume ls
```


- **docker network create**: Crea una red para que los contenedores puedan comunicarse entre ellos y así no tener que centralizar dos servicios en un contenedor.

```bash
docker network create mi-red
```


- **docker network ls**: Lista todas las redes.

```bash
docker network ls
```


## Gestión de Docker Compose


- **docker compose up**: Construye, crea e inicia todos los servicios definidos en el archivo `docker-compose.yml`.

```bash
docker compose up
```


- **docker compose down**: Detiene y elimina los contenedores, redes y volúmenes.

```bash
docker compose down
```


- **docker compose ps**: Lista los contenedores de los servicios definidos.

```bash
docker compose ps
```


- **docker compose logs**: Muestra las salidas de los servicios, errores e información de los contenedores.

```bash
docker compose logs
```
