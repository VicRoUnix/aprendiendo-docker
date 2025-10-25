# Learn Docker Compose

## Anatomia moderna del docker-compose.yml
```
yml
# ✅ SIN version: - Docker Compose V2 detecta automáticamente la mejor versión
services:
  frontend:
    build: 
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
    networks:
      - app-network
    restart: unless-stopped

  db:
    image: mongo:7-jammy
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password123
    volumes:
      - mongo_data:/data/db
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
    name: mi-app-network

volumes:
  mongo_data:
    driver: local
    name: mi-app-mongo-data
```
Este archivo docker-compose.yml define y configura servicios de contenedores DOcker para facilitar el despligue y la orquestacion de aplicaciones.
Permite levantar multiples servicios,especificar redes, volumnes y variables de entorno, simplificando el desarrollo y la administracion de entornos multi-contenedor.

### Propiedades principales del docker-compose.yml

- services:
	Define los servicios(contenedores) que forman tu aplicacion. Cada clave bajo `services` es un servicio independiente.
	- frontend:
		Servicio para la aplicacion frontend (por ejemplo, React.)
		- build:
			- context: Carpeta donde esta el codigo fuente a contruir.
			- dockerfile: Archivo Dockerfile a usar para contruir la imagen.
		- ports: 
			- "3000:3000": Expone el puerto 3000 del contenedor al 3000 de tu maquina
		- enviroment:
			- Variables de entorno para el contendor: (ejemplo: URL de la API)
		- dependes_on:
			- Indica que este servicio depende de que otro (ej:backend) este listo antes de iniciar.
		- networks:
			- Redes a las que se conecta el servicio
		- restart:
			- Politica de reinicio automatico si el contenedor se detiene 
	- db:
		Servicio para la base de datos MongoDB.
		- image: 
			- Imagen de Docker a usar (ej:mongo7-jammy)
		- ports:
			- "2707:27017: Expone el puerto estandar de MongoDB.
		- enviroment:
			- Varaibles de entorno para inicializar MongoDB (usuario y contraseña).
		- volumnes:
			- MOnta un volumen persistente para los datos de la base.
		- networks:
			- Redes a las que se conecta el servicio.
		- healthcheck:
			- Prueba periodica para verificar que MongoDB esta listo y responde.
		- restart:
			- Politica de reinicio automatico.
	- networks:
		Define redes personalizadas para aislar y conectar servicios entre si.
	- volumes:
		Define volumenes persistentes para que los datos no se pierdan si el contenedor se elimina.

---

## Comandos esenciales de Docker Compose V2

### Comandos basicos
```
bash

# Levantar todos los servicios
docker compose up

# Modo detached (en segundo plano)
docker compose up -d

# Reconstruir imagenes antes de levantar
docker compose up --build

# Levantar servicios especificos
docker compose up frontend backend

# Ver estados de servicios
docker compose ps

# Ver logs en tiempo real
docker compose logs -f

# Ver logs de un servicio especifico
docker compose logs -f backend

# Parar servicios sin eliminar contenedores
docker compose stop

# Parar y eliminar contenedores, redes y volumenes anonimos
docker compose down

# Eliminar tambien volumenes nombrados
docker compose down --volumes

# Eliminar todo incluyendo imagenes
docker compose down --rmi all --volumes
```

### Comandos avanzados
```
bash
# Ejecutar comandos en servicios corriendo
docker compose exec backend npm run test
docker compose exec db mongosh

# Ejecutar comandos sin servicio corriendo
docker compose run --rm backend npm install

# Escalar servicios (crear multiplies instancias)
docker compose up --scale backend=3

# Ver configuracion parseada
docker compose config

# Validar archivo compose
docker compose config --quiet

# Reiniciar servicios especificos
docker compose restart nginx

# Ver uso de recursos
docker compose top
```

---

##Realizar un WordPress con Docker Compose
```
yml
# WordPress Moderno con Docker COmpose V2+
services:
  wordpress:
    image: wordpress:php8.2-apache
    container_name: wp-web
    deploy:
       resources:
          limits:
            cpus: '1'
            memory: 512M
    restart: unless-stopped
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db
      WORDPRESS_DB_USER: /run/secrets/db_user
      WORDPRESS_DB_PASSWORD: /run/secrets/db_pass
      WORDPRESS_DB_NAME: /run/secrets/db_name
    volumes:
      - wp_data:/var/www/html
      - ./wp-content:/var/www/html/wp-content  # Para desarrollo personalizado
    depends_on:
      db:
        condition: service_healthy
    networks:
      - wp_network

  db:
    image: mariadb:11.3
    container_name: wp-db
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: /run/secrets/db_root_pass
      MYSQL_DATABASE: /run/secrets/db_name
      MYSQL_USER: /run/secrets/db_user
      MYSQL_PASSWORD: /run/secrets/db_pass
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD-SHELL", "mariadb-admin ping -h localhost -u$$(cat /run/secrets/db_user) -p$$(cat /run/secrets/db_pass)"]
      interval: 5s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - wp_network

  phpmyadmin:
    image: phpmyadmin:latest
    container_name: wp-admin
    restart: unless-stopped
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
      PMA_USER_FILE: /run/secrets/db_user
      PMA_PASSWORD_FILE: /run/secrets/db_pass
    depends_on:
      - db
    networks:
      - wp_network

volumes:
  wp_data:
  db_data:

networks:
  wp_network:
    driver: bridge

secrets:
  db_root_pass:
    file: ./secrets/db_root_pass.txt
  db_name:
    file: ./secrets/db_name.txt
  db_user:
    file: ./secrets/db_user.txt
  db_pass:
    file: ./secrets/db_pass.tx
```
## Características clave

### Stack Completo
	- WordPress (última versión PHP 8.2)
	- MariaDB 11.3 (alternativa óptima a MySQL)
	- phpMyAdmin para gestión de bases de datos

### Buenas Prácticas
	- Volúmenes persistentes para datos y DB
	- Healthcheck en MariaDB
	- Variables de entorno separadas
	- Red aislada para seguridad

### Configuración para Desarrollo
	- Mapeo directo de `wp-content` para temas/plugins
	- Puertos accesibles:
    		- **WordPress:** [http://localhost:8080](http://localhost:8080)
    		- **phpMyAdmin:** [http://localhost:8081](http://localhost:8081)

---

## Cómo usarlo

1.  Crea un directorio y guarda el archivo como `docker-compose.yml`.
2.  Ejecuta:
    ```bash
    docker compose up -d
    ```
3.  Accede a WordPress en tu navegador y completa la instalación.

---

##  Notas importantes

### Seguridad en Producción
	- Cambia todas las contraseñas.
	- Usa **secrets** para las credenciales:
    		```yaml
    		secrets:
      			db_root_pass:
   				file: ./secrets/db_root_pass.txt
  			db_name:
    				file: ./secrets/db_name.txt
  			db_user:
    				file: ./secrets/db_user.txt
  			db_pass:
    				file: ./secrets/db_pass.tx

    ```

### Performance
	- Para alta demanda, añade límites de recursos:
    		```yaml
    		wordpress:
      			deploy:
        			resources:
          				limits:
            					cpus: '1'
            					memory: 512M
   		 ```

---

## Comandos útiles

| Comando | Descripción |
| :--- | :--- |
| `docker compose logs -f wordpress` | Ver logs en tiempo real |
| `docker compose exec db mysql -u wpuser -p` | Acceder a la CLI de MySQL |
| `docker compose down --volumes` | Borrar TODO (incluyendo datos) |

---


## Trucos y mejores practicas

### 1.Healthchecks inteligentes
```
yml
services:
	api:
		healthcheck:
			test:["CMD", "curl", "-f", "http://localhost:3000/health"]
			interval: 30s
			timeout: 10s
			retries: 3
			start-period: 60s
```

### 2.Depends_on con condiciones
```
yml
services:
	app:
		depends_on:
			db:
				condition: service_healthy
			redis:
				condition: service_started
```

### 3.Variables de entorno avanzadas
```
services:
	app:
		enviroment:
			- NODE_ENV=${NODE_ENV:-development}
			- PORT=${APP_PORT:-3000}
			- DATABASE_URL=${DATABASE_URL:?error}
```

### 4.Extension de configuraciones
```
yml
# docker-compose.yml
services:
  	app: &app
    		build: .
    			environment:
      				- NODE_ENV=production

# docker-compose.override.yml (para desarrollo)
services:
  	app:
    		<<: *app
    			environment:
      				- NODE_ENV=development
    			volumes:
     				- .:/app
```

---

## Debugging y troubleshooting

### Comandos utiles para debugging
```
bash
# Ver configuracion final parseada
docker compose config

# Inspeccionar redes
docker network ls
docker network inspect mern-app-network

# Ver volúmenes
docker volume ls
docker volume inspect mern-mongo-data

# Logs detallados con timestamps
docker compose logs -f --timestamps

# Ver procesos dentro de contenedores
docker compose top

# Estadísticas de uso
docker stats $(docker compose ps -q)

# Acceder a shell de contenedor
docker compose exec backend bash
docker compose exec db mongosh
```

## Problemas comunes y soluciones

### 1.Puerto ya en uso:
```
bash
# Ver que proceso usa el puerto
lsof -i :3000
# Cambiar puerto en .env o docker-compose.yml
```

### 2.Problemas de red
```
bash
# Recrear redes
docker compose down
docker network prune
docker compose up
```

### 3.Volumenes corruptos
```
bash
# Limpiar volúmenes
docker compose down --volumes
docker volume prune
```

---

# TAREA: Aplicacion Node.js + MongoDB con Docker compose 

## Parte 1: Configuracion Basica
### 1.Estructura del proyecto
```
bash
mkdir node-mongo-app && cd node-mongo-app
mkdir backend
touch backend/{server.js,package.json,Dockerfile} docker-compose.yml
```

### 2.Archivos Base:
- backend/server.js
```
js
const express = require('express');
const mongoose = require('mongoose');
const app = express();

mongoose.connect('mongodb://db:27017/mydb');

app.get('/', (req, res) => {
  res.send('¡API conectada a MongoDB con Docker!');
});

app.listen(3000, () => console.log('Server running on port 3000'));
```
- backend/Dockerfile
```
FROM node:18-alpine
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

### 3.docker-compose.yml
```
yml
services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
  
  db:
    image: mongo:6
    volumes:
      - db_data:/data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  db_data:
```

## Parte 2:Ejecucion y verificacion
### 1.Inicia los servicios
``` 
bash
docker compose up -d
```
- Si falla la base de datos prueba con mongo:4.4

### 2.Prueba la API
```
bash
curl http://localhost:3000
# Deberías ver: "¡API conectada a MongoDB con Docker!"
```

### 3.Verificar la base de datos
```
bash
docker compose exec db mongosh --eval "show dbs"
```

## Parte 3: Persistencia y Debugging
### 1.Deten y reinicia los contendores
```
bash
docker compose down && docker compose up -d
```

### 2.Verifica los datos de MongoDB persistan 
- Crea una coleccion:
```
bash
docker compose exec db mongosh --eval "db.test.insertOne({name: 'Pepe'})"
```
- Reinicia y comprueba que siga existiendo.

#Bonus
### Añade un frontend con React:
1.Agregar al docker-compose.yml
```
yml
frontend:
  image: node:18-alpine
  working_dir: /app
  volumes:
    - ./frontend:/app
  ports:
    - "5173:5173"
  command: ["npm", "run", "dev"]
  depends_on:
    - backend
```
---

