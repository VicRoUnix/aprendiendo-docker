
# Bases para generar una imagen Docker


Se genera un archivo llamado `Dockerfile` que contiene instrucciones de los comandos que tendrá que correr.


## Instrucciones comunes


- **FROM <image>**: Siempre debe tener el comando FROM, ya que especifica de qué imagen proviene y si vamos a añadir más contenido o no.

```dockerfile
FROM python:3.13
```
*Observar que se tiene que especificar el tag después de los dos puntos (:) si se quiere tener una versión en concreto.*


- **WORKDIR <path>**: Especifica cuál será el directorio de trabajo o la ruta de la imagen donde los archivos serán copiados y los comandos se ejecutarán.

```dockerfile
WORKDIR /usr/local/app
```
*Buenas prácticas para estipular el directorio:*
  - Usar un nombre simple y claro: nombres como **/app**, **/usr/src/app** o **/code** son los más comunes. Para aplicaciones, **/app** es una elección muy común.
  - No usar la raíz **(/)** como directorio de trabajo.


- **COPY <host-path> <image-path>**: Esta instrucción le dice al constructor que copie los archivos de una ruta del host y los ponga en la carpeta del contenedor de la imagen.

```dockerfile
COPY ./python_scripts /usr/local/app
COPY ./requirements.txt .
```


- **RUN <command>**: Con esta instrucción le dice al constructor que ejecute unos comandos específicos.

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
*La bandera `--no-cache-dir` le dice a pip que no use la caché local para la instalación. Normalmente, cuando se instala un paquete con pip, lo guarda en la caché del disco duro.*
*La bandera `-r` indica que instale los paquetes desde un archivo de requisitos. Esta bandera permite listar todas las dependencias de un proyecto en un solo archivo.*


- **ENV <name> <value>**: Esta instrucción declara variables de entorno que el contenedor usará.

```dockerfile
ENV DB_HOST=db.production.com
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
```


- **USER <user-or-id>**: Esta instrucción define cuál será el usuario para todos los comandos posteriores.

```dockerfile
USER app
```


- **CMD ["<comando>", "<arg1>"]**: Esta instrucción declara cuáles serán los comandos que el contenedor use cuando la imagen se ponga a funcionar, es decir, su propósito es iniciar el proceso principal del contenedor.

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```
* **uvicorn**: Es un ejecutable, un servidor ASGI popular de Python.
* **app.main:app**: Le indica a uvicorn que en el directorio `app` busque un archivo llamado `main.py` y que dentro de ese archivo debe buscar y ejecutar la instancia de la aplicación que se llama `app`.
* **--host "0.0.0.0"**: Argumento que indica a Uvicorn que el servidor debe escuchar en todas las interfaces de red disponibles. Docker solo escucha en 127.0.0.1 (localhost), el servidor solo se podría acceder dentro del propio contenedor. Con este argumento hacemos que sea accesible desde el exterior, usando `docker run -p`.
* **--port "8080"**: Este argumento especifica el puerto en el que el servidor debe escuchar. La aplicación estará funcionando en el puerto 8080.

