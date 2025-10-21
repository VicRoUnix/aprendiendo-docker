#Ejecutar contenedor en segundo plano -d que le diga que escriba Hello world durante 1 segundo
```
bash
docker run -d --name contenedor2 ubuntu bash -c "while true; do echo hello world; sleep 1; done"
```
#Ver que contenedor esta en marcha
```
bash
docker ps
```
#Ver que esta haciendo
```
bash
docker logs contenedor2
```
#Detener y eliminar el contenedor o eliminar sin detenerlo el contenedor
```
bash
docker stop contenedor2
docker rm contenedor2
docker rm -f contenedor2
```
#Ciclo de vida de contenedores
```
bash
docker run -d --name hora-container ubuntu bash -c 'while true; do echo $(date + "%T"); sleep 1; done'
docker logs -f hora container
```
#Ejecutar comandos dentro del contenedor
```
bash
docker exec hora-container date
```
#Crear un nuevo contenedor que guarde la hora en un archivo
```
bash
docker run -d --name hora-container2 ubuntu bash -c 'while true; do date +"%T" >> hora.txt; sleep 1; done'
docker exec hora-container2 ls
docker exec hora-conatiner2 cat hora.txt
```
#Copiar archivos entre host y contenedor
#DEsde el host hacia el contenedor
```
bash
echo "Curso Docker" > docker.txt
docker cp docker.txt hora-container2:/tmp
docker exec hora-container2 cat /tmp/docker.txt
```
#Desde el contenedor hacia el host
```
bash
docker cp hora-container2:hora.txt .
```
#Procesos y detalles del contenedor
#Ver procesos en ejecucion
```
bash
docker top hora-container2
```
#Inspeccionar contenedor (JSON detallado)
```
bash
docker inspect hora-container2
```
#Filtros utiles con --format:
#Id del contendor
```
bash
docker inspect --format='{{.Id}}' hora-container2
```
#Imagen usada
```
bash
docker inspect --format='{{.Config.Image}}' hora-container2
```
#Variables de entorno
```
bash
docker container inspect -f '{{range.Config.Env}}{{println .}}{{end}}' hora-container2
```
#Comando ejecutado
```
bash
docker inspect --format='{{range.Config.Cmd}}{{println .}}{{end}}' hora-container2
```
#Ip asignada
```
bash
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' hora-container2
```
#Configuracion de contenedores con variables de entorno
```
bash
docker run -it --name prueba -e USUARIO=prueba ubuntu bash
echo $USUARIO
```
#Configuracion de un contenedor con la imagen mariadb
#Algunas imagenes como mariadb, requieren variables para inicializarse.Segun la documentacion una variable obligatoria es
```
bash
docker run -d --name some-mariadb -e MARIADB_ROOT_PASSWORD=my-secret-pw mariadb
```
#Verificar la variable dentor del contenedor
```
bash
docker exec -it some-mariadb env
```
#Accedemos a MariaDB desde el contenedor
```
bash
docker exec -it some-mariadb -u root -p
```
#Accediendo a MariaDB desde el exterior
#Eliminar contenedor anterior
```
bash
docker rm -f some-mariadb
```
#Crear un nuevo contendor mariadb exponiendo el puerto
```
bash
docker run -d -p 3306:3306 --name some-mariadb -e MARIADB_ROOT_PASSWORD=my-secret-pw mariadb
```
#Accedemos desde el host(requiere tener instalado el cliente de mariadb)
```
bash
mysql -u root -p -h 127.0.0.1
```
#DESAFIO DEL DIAA
#1.Crea un contenedor personalizado que cada 5 segundos escriba un mensaje diferente (puede ser la hora, un contador o un texto aleatorio) en un archivo llamado mensajes.txt
#2.Copia el archivo mensajes.txt desde el contenedor al host y verifica su contenido.
#3.Utiliza docker inspect para obtener la IP del contenedor y el nombre de la imagen utilizada.
#4.Comprueba los procesos activos dentro del contenedor usando docker top y verifica que el proceso principal sigue ejecutándose
#5.Detén y elimina el contenedor de forma forzada usando un solo comando
#6.Automatiza los pasos anteriores con un pequeño script bash
