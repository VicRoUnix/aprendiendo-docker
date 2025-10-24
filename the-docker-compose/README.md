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
