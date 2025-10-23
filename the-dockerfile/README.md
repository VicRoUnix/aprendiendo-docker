# Que es un Dockerfile?
- Un Dockerfile es un archivo de texto que contiene instrucciones para construir una imagen Docker paso a paso.
Cada instrucción agrega una capa a la imagen.

---

# Estructura minima de una imagen
## 1.Crear un nuevo directorio
```
bash
mkdir simple-nginx && cd simple-nginx
```
## 2.Crear o copiar archivo HTML(index.html)
```
html
<h1>Hola soldado devOps esta es mi propia imagen de nginx</h1>
```
## 3.Crear archivo Dockerfile
```
bash
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

---

# Instrucciones basicas del Dockerfile
| Instruccion | Para que sirve? | Ejemplo
|---|---|---|
| `FROM` | Define la imagen base. Siempre es la primera instruccion. | `FROM node:18-alpine` |
| `WORKDIR` | Establece el directorio de trabajo dentro del contenedor. | `WORKDIR /app` |
| `COPY` | Copia archivos del hsot al contenedor | `COPY . /app` |
| `ADD` | Igual que `COPY`, pero permite descomprimir `.tar` o descargar desde URL. | `ADD archivo.tar.gz /app` |
| `RUN` | Ejecuta comandos en la copnstruccion de la imagen. | `RUN npm install` |
| `CMD` | Define el comando por defecto al ejecutar el contenedor | `CMD ["npm, "start"]` | 
| `ENTRYPOINT` | Similar a `CMD`,pero no se sobreescribe facilmente. Ideal para comandos fijos. | `ENTRYPOINT ["node", "index.js"]` |
| `ENV` | Define variables de entorno dentro del contenedor. | `ENV PORT=3000` |
| `EXPOSE` | Documenta el puerto que la app escucha (no abre el puerto). | `EXPOSE 8080` |
| `LABEL` | Añade metadatos a la imagen. | `LABEL maintainer="vic@example.com"` |
| `VOLUME` | Crea un punto de montaje para persistencia. | `VOLUME /data` | 
| `ARG` | Define variables disponibles solo durante la build. | `ARG VERSION=1.0` | 
| `USER` | Define el usuario que ejecuta los comandos dentro del contenedor. | `USER node` |
| `HEALTHCHEK` | Define como Docker verifica que el contenedor esta sano. | `HEALTHCHECK CMD curl --fail http://localhost:3000` |

---

# Construir tu imagen Docker 
Ejecutara el siguioente comando en el mismo directorio donde esta tu Dockerfile
```
bash
docker build -t simple-nginx:v1 .
```
- `-t`: Define el nombre y la version/tag de la imagen
- `.`: Indica que el contexto de build es el directorio actual
# Verificar tu imagen
- Listar imagenes disponibles
```
bash
docker images
```
- Ver el historial de capas
```
bash
docker history simple-nginx:v1
```
- Inspeccionar detalles de la imagen
```
bash
docker inspect simple-nginx:v1
```

---

#Ejecutar un contenedor desde tu imagen
```
bash
docker run -d --name my-nginx -p 8080:80 simple-nginx:v1
```
- `-d`: Ejecutar en segundo plano
- `--name`: Asignar nombre al contenedor
- `-p 8080:80`: Mapea el puerto 80 del contenedor al 8080 local

---

#Limpiar recursos
- Eliminar contenedor
```
bash
docker rm -f my-nginx
```
- Eliminar imagen
```
bash
docker rmi simple-nginx:v1
```
- Eliminar imagenes no utilizadas
```
bash
docker image prune -a
```

---

# Buenas practicas basicas para tu Dockerfile
- Usa imagenes base livianas (alpine,distroless,etc.)
- Siempre limpia archivos temporales en `RUN`.
- Agrupa comandos para reducir capas
- Usa `.dockerignore` para excluir archivos innecesarios
Ejemplo de `.dockerignore`
```
bash
.git
node_modules
*.log
```

---

#Contruccion de una Imagen Docker de una aplicacion Node.js
Este ejemplo crea una imagen Docker para una app basica de Node.js que devuelve un saludo en un endpoint HTTP
## 1.Crea una carpeta del proyecto
```
bash
mkdir hello-node && cd hello-node
```
## 2.Crea el archivo index.js
```
js
const http = require('http');

const PORT = process.en.PORT || 3000;

http.createServer((req, res) => {
	res.writeHead(200, { 'Content-Type': 'text/plain' });
	res.end('Hola desde Docker y Node.js!\n');
}).listen(PORT);

console.log(`Servidor corriendo en http://localhost:${PORT}`);
```
## 3.Crea un package.json
```
js
{
  "name": "hello-node",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  }
}
```
## 4.Instala las dependencias
```
bash
npm install
```
## 5.Crea el archivo Dockerfile
```
bash
FROM node:18-alpine
WORKDIR /app
COPY package.json ./
COPY index.js ./
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
```
## 6.Construye tu imagen
```
bash
docker build -t hello-node-app .
```
## 7.Ejecuta tu contenedor
```
bash
docker run -d --name hello-app -p 3000:3000 hello-node-app
```
- Navega a: http://localhost:3000

---

# Tarea del dia
## 1. Crea un directorio simple-nginx
```
bash
mkdir simple-nginx && cd simple-nginx
```
## 2.Escribir un archivo index.html con tu propio mensaje
```
html
<h1> Use mi propio index.html </h1>
```
## 3.Crea un Dockerfile como el del ejemplo
```
bash
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```
## 4.Construi la imagen usando docker build
```
bash
docker build -t simple-nginx:v1
```
## 5.Ejecutar el contenedor y verificar que la pagina web aparece en http://localhost:8080
```
bash
docker run -d --name web-app -p 8080:80 simple-nginx:v1
```

# Conectar contenedores
## 1. Ahora vas a crear una imagen python desde 0, para ello crea una nueva carpeta para la imagen
``` 
bash
mkdir simple-py-app && cd simple-py-app
```
## 2.Crear el fichero app.py donde estara nuestra aplicacion python
```
bash
cat app.py
```
## 3.Crear el fichero requirements.txt para ver que requisitos queremos para la app
```
bash
cat requirememts.txt
```
## 4.Crear el Dockerfile de nuestra aplicacion python
```
bash
FROM python:3.7-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 80
ENV MY_APP_VERSION="1.0"
CMD ["python", "app.py"] 
```
## 5.Construir imagen python-app
```
bash
docker build -t pysql-app:v1 .
```
## 5.Salir de la carpeta de la appy.py y crear una red para el desafio
```
bash
cd ..
docker network create test-web
```
## 6.Crear contenedor mysql para la prueba
```
bash
docker run -d --name mi-mysql-db --network test-web -e MYSQL_ROOT_PASSWORD=myps -e MYSQL_DATABASE=test_db  mysql
```
## 7.Crear contenedor python
```
bash
docker run -d --name mi-app-web -p 8080:80 --network test-web -e MYSQL_HOST=mi-mysql-db pysql-app:v1
```
## 8.Visitar la web http://localhost:8080
## 9.Ver si se conecta correctamente con la base de datos mysql visitar http://localhost:8080/connect 

