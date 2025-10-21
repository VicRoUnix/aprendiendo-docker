#!/bin/bash

#1.Crearemos el contenedor personalizado que escriba mensajes cada 5 segundos
#Creamos contendor
echo "Creando contenedor de mensajes..."
docker run -d --name mensajero ubuntu bash -c '
mensajes=("$(date)" "Hello world" "DevArmenScript" "AmazingSpiderman")
i=0
#Comenzamos bucle
while true; do 
	echo "${mensajes[i]}" >> mensajes.txt
	i=$(( (i + 1) % ${#mensajes[@]} ))
	sleep 5
done
'

#2. Copiar el archivo mensajes.txt desde el contenedor hacia el host y verificar el contenido
echo "Copiando archivo mensajes para su revision"
docker cp mensajero:mensajes.txt .
echo "Visualizando mensajes..."
cat mensajes.txt

#3. Utilizar Docker inspect para obtener la IP del contenedor y el nombre de la imagen utilizada
echo "Obteniendo ip y nombre de la imagen del contendor mensajero"
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mensajero
docker inspect -f '{{.Config.Image}}' mensajero

#4. Comprovar que procesos activos hay activos en el contenedor y si todavia sigue el principal ejecutandose
echo "Visualizando procesos activos del contenedor..."
docker exec mensajero top -b -n 1
echo "Fijarse si se esta ejecutando el comando en bash"

#5. Detener y eliminar el contenedor con un solo comando
echo "Ver si el contenedor esta activo"
docker ps
echo "Eliminando el contenedor de mensajero"
docker rm -f mensajero
docker ps
echo "Se elimino correctamente"
