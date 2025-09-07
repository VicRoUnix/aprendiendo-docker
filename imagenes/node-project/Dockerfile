#Imagen de el repositorio oficial de DockerHub de node
FROM node:24-alpine3.21

#Crear el directorio de la aplicacion
WORKDIR /app

#Copiar los archivos de la aplicacion al contenedor
COPY . .

#Instalar las dependencias de la aplicacion
RUN npm install

#Exponer el puerto en el que la aplicacion va a correr
EXPOSE 8080

#Comando para correr la aplicacion
CMD ["node", "app.js"]