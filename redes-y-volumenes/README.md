#Tipo de redes en Docker
- bridge: Red por defecto para contenedores en una misma maquina
- host: El contedor comparte la red del host (sin aislamiento de red)
- none: Sin red. El contenedor no se conecta a ninguna red
- overlay: Usado con Docker Swarm para comunicar contendores entre multiples hosts
- macvlan: Asigna una IP desde la red del host. Util para apps legacy

---

#Ver todas las redes disponibles
```
bash
docker networks ls
``` 
#Crear y usar una red personalizada
``` 
bash
docker network create mi-red
docker run -d --name backend --network mi-red alpine sleep 3600
docker run -it --rm --network mi-red alpine ping backend
```
#Inspeccionar y eliminar redes
```
docker network inspect mi-red
docker network rm mi-red
```

---

#Tipos de volumenes
- volumenes gestionados(docker volume): Se guardan en la ruta /var/lib/docker/volumes del host // Se utilizan para compartir datos entre contenedores
- bind mounts: Se guardan en cualquier ruta del host (ej:./datos)// Se utilizan para desarrollo local, sincornizacion en vivo
- tmpfs: Se guardan en la memoria RAM (temporal) // Se utilizan para apps sensibles que no necesitan persistencia

#Crear y usar un volumen
```
bash
docker volume create datos-app
docker run -d --name contenedor-volumen -v datos-app:/datos alpine sh -c "while true; do date >> /datos/fechas.log; sleep 5; done" 
docker exec contenedor-volumen cat /datos/fechas.log
```
#Ver volumenes disponibles
```
bash
docker volume ls
```
#Eliminar un volumen (si no esdta en uso)
```
bash
docker volume rm datos-app
```
#Bind mounts (montar directorios del host)
```
bash
mkdir datos-local
docker run -it --name con-mount -v $(pwd)/datos-local:/datos alpine sh
```

---

#Comandos utiles de redes y volumenes
#Redes
```
bash
docker network create <nombre>
docker network ls
docker network inspect <nombre>
docker network rm <nombre>
docker network connect <red> <contenedor>
docker network disconnect <red> <contenedor>
```

#Volumenes
```
bash
docker volume create <nombre>
docker volume ls
docker volume inspect <nombre>
docker volume rm <nombre>
```

---

#Ejemplo: MYSQL con Docker
#1. Crear el contenedor con volumen persistente
```
bash
docker run -d --name mysql-container \
	-e MYSQL_ROOT_PASSWORD=my-data-pass \
	-v /data/mysql-data:/var/lib/mysql \
	mysql
```
#2. Acceder al contenedor
```
bash
docker exec -it mysql-container bash
mysql -u root -p
```
#3. Ejecutar un script SQL (dentro del contenedor)
```
bash
CREATE DATABASE base_de_datos;
USE base_de_datos;
```
#4. Detener y eliminar el contenedor
```
bash
docker stop mysql-container
docker rm mysql-container
```
#5. Reiniciarlo y verificar que los datos persisten
```
bash
docker run -d --name mysql-container \
        -e MYSQL_ROOT_PASSWORD=my-data-pass \
        -v /data/mysql-data:/var/lib/mysql \
        mysql

docker exec -it mysql-container bash
mysql -u root -p
USE base_de_datos;
SELECT * FROM usuarios;
```

---

#Desafio de apredizaje
# 1.Crea una red personalizada miapp-net
# 2.Ejecutar dos contenedores api y db en esa red
# 3.Desde api, hace ping a db para verificar conectividad.
# 4.Crear un volumen vol-db y montarlo en /datos dentro del contenedor db
# 5.Desde db, escribi un archivo en /datos/info.txt
# 6.Elimina el contenedor db, vuelve a crearlo y comprobar si el archivo sigue existiendo


#Reto 1
```
bash
docker network create miapp-net
```
#Reto 2
```
bash
docker run -d --name api --network miapp-net nginx
docker run -d --name db --network miapp-net -e MYSQL_ROOT_PASSWORD=my-ps mysql
```
#Reto 3
```
bash
docker exec -it api bash
apt-get update
apt-get install -y iputils-ping
exit
docker exec api ping db
```
#Reto 4
```
bash
docker volume create vol-db
docker rm -f db
docker run -d --name db --network miapp-net -v vol-db:/datos -e MYSQL_ROOT_PASSWORD=myps mysql
```
#Reto 5
```
bash
docker exec db touch /datos/info.txt
docker exec db sh -c 'echo "Esto es una prueba" > /datos/info.txt'
```
#Reto 6
```
bash
docker rm -f db
docker run -d --name db --network miapp-net -v vol-db:/datos -e MYSQL_ROOT_PASSWORD=myps mysql
docker exec db ls /datos/
docker exec db cat /datos/info.txt
```
#Reto Adicional: MongoDB + Mongo Express
#Crear dos contenedores, MOngoDB y MongoExpress y conectarlos con Docker
# 1. Crear contenedor MongoDB
```
bash
docker run -d --name mongo -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret --network miapp-net mongo
```
# 2. Crear contenedor de Mongo Express
```
bash
docker run -d --name mongo-express -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin -e ME_CONFIG_MONGODB_ADMINPASSWORD=secret -e ME_CONFIG_MONGODB_SERVER=mongo -p 8081:8081 --network miapp-net mongo-express
```
# 3.acceder a la interfaz web en: http://localhost:8081

# 4.Crear la base de datos Library y la coleccion Books en la web.

# 5.Importar datos (books.json) y cargarlos desde la web en mongo-express
```
bash
#Copiar y pegar
[
  { "title": "Docker in Action, Second Edition", "author": "Jeff Nickoloff and Stephen Kuenzli" },
  { "title": "Kubernetes in Action, Second Edition", "author": "Marko Lukša" }
]
#Salir del archivo

