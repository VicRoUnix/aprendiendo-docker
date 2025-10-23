import os
import mysql.connector
import time
from flask import Flask

app = Flask(__name__)

# Función para intentar conectar a MySQL
def get_db_connection():
    # El 'host' es el nombre que le darás a tu contenedor de MySQL
    # Docker se encargará de resolver este nombre a la IP correcta.
    db_host = os.environ.get('MYSQL_HOST', 'mi-mysql-db') 
    db_user = os.environ.get('MYSQL_USER', 'root')
    db_pass = os.environ.get('MYSQL_ROOT_PASSWORD', 'myps') # La contraseña de tu otro contenedor
    db_name = os.environ.get('MYSQL_DATABASE', 'test_db')

    # --- Bucle de reintento ---
    # Esto es crucial. La app web puede empezar más rápido que la DB.
    retries = 15
    while retries > 0:
        try:
            print(f"Intentando conectar a MySQL en {db_host}...")
            conn = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database=db_name
            )
            print("¡Conexión exitosa!")
            return conn
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            retries -= 1
            time.sleep(3) # Espera 3 segundos antes de reintentar
    
    print("Fallo al conectar después de varios reintentos.")
    return None

@app.route('/')
def hello():
    return "¡Hola! Esta es la app de Python."

@app.route('/connect')
def test_connection():
    conn = get_db_connection()
    if conn:
        conn.close()
        return "¡CONEXIÓN A MYSQL EXITOSA!"
    else:
        return "FALLO AL CONECTAR A MYSQL.", 500

if __name__ == "__main__":
    # Escucha en el puerto 80 (como se expuso en el Dockerfile)
    # y en '0.0.0.0' para ser accesible desde fuera del contenedor.
    app.run(host='0.0.0.0', port=80)
