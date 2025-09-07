// Importa el framework Express
const express = require('express');

// Crea una instancia de la aplicación Express
const app = express();

// Define el puerto donde se ejecutará el servidor
const port = process.env.PORT || 3000;

// Middleware para servir archivos estáticos (CSS, JS, imágenes)
app.use(express.static('public'));

// Define una ruta para la página principal
app.get('/', (req, res) => {
  // Envía la página HTML
  res.send(`
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>DevOps Junior - Portafolio</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          background-color: #f0f2f5;
          color: #333;
          text-align: center;
          padding-top: 50px;
        }
        .container {
          background-color: #fff;
          padding: 20px 40px;
          border-radius: 8px;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
          max-width: 600px;
          margin: auto;
        }
        h1 {
          color: #007bff;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>¡Hola! Soy un Ingeniero DevOps Junior 🚀</h1>
        <p>Esta es mi primera página web usando Docker y Node.js.</p>
        <p>Estoy aprendiendo a crear, contenerizar y desplegar aplicaciones.</p>
        <p>Contáctame para más información.</p>
        <a href="https://linkedin.com" target="_blank">Mi LinkedIn</a>
      </div>
    </body>
    </html>
  `);
});

// Inicia el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});