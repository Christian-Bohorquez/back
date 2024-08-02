Manual Técnico
Índice
Requisitos del Sistema
Configuración del Entorno
Estructura del Proyecto
API Backend
Instalación
Modelos
Rutas
Migraciones de la Base de Datos
Frontend
Instalación
Servicios
Componentes
Pruebas
Despliegue
Requisitos del Sistema
Python 3.12
Node.js 14.x o superior
PostgreSQL 13.x o superior
Docker (opcional, para ejecución en contenedores)
Configuración del Entorno
Backend
Clonar el repositorio:

bash
Copiar código
git clone <repositorio-url>
cd backend
Crear y activar un entorno virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instalar dependencias:

bash
Copiar código
pip install -r requirements.txt
Configurar variables de entorno:
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

env
Copiar código
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_base_de_datos>
JWT_SECRET_KEY=tu_secreto_jwt
Inicializar la base de datos:

bash
Copiar código
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Ejecutar la aplicación:

bash
Copiar código
flask run
Frontend
Clonar el repositorio (si no lo has hecho):

bash
Copiar código
git clone <repositorio-url>
cd frontend
Instalar dependencias:

bash
Copiar código
npm install
Configurar variables de entorno:
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

env
Copiar código
REACT_APP_API_URL=http://localhost:5000/api
Ejecutar la aplicación:

bash
Copiar código
npm start
Estructura del Proyecto
Backend
bash
Copiar código
backend/
├── app.py
├── models.py
├── routes.py
├── __init__.py
├── migrations/
├── requirements.txt
└── .env
Frontend
bash
Copiar código
frontend/
├── public/
├── src/
│   ├── components/
│   │   └── Register.js
│   ├── services/
│   │   └── authService.js
│   ├── App.js
│   ├── index.js
│   └── .env
├── package.json
└── .env
API Backend
Instalación
Asegúrate de seguir los pasos de Configuración del Entorno para instalar todas las dependencias necesarias y configurar las variables de entorno.

Modelos
models.py
Define los modelos de datos usando SQLAlchemy.

python
Copiar código
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(256), nullable=False)
    carrera = db.Column(db.String(100), nullable=False)
    año_de_ingreso = db.Column(db.Integer, nullable=False)

    @property
    def contraseña(self):
        raise AttributeError('contraseña is not a readable attribute')

    @contraseña.setter
    def contraseña(self, contraseña):
        self.contraseña_hash = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña_hash, contraseña)
Rutas
routes.py
Define las rutas de la API usando Flask.

python
Copiar código
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from models import db, Usuario

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

db.init_app(app)
jwt = JWTManager(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        contraseña=data['contraseña_hash'],
        carrera=data['carrera'],
        año_de_ingreso=data['año_de_ingreso']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"msg": "Usuario registrado con éxito"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data['email']).first()
    if usuario and usuario.verificar_contraseña(data['contraseña']):
        access_token = create_access_token(identity={'email': usuario.email})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run()
Migraciones de la Base de Datos
Las migraciones permiten gestionar los cambios en la estructura de la base de datos.

bash
Copiar código
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
Frontend
Instalación
Asegúrate de seguir los pasos de Configuración del Entorno para instalar todas las dependencias necesarias y configurar las variables de entorno.

Servicios
authService.js
Define las llamadas a la API para la autenticación.

javascript
Copiar código
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

const register = (nombre, email, contraseña, carrera, año_de_ingreso) => {
    return axios.post(`${API_URL}/register`, { nombre, email, contraseña_hash: contraseña, carrera, año_de_ingreso });
};

const login = (email, contraseña) => {
    return axios.post(`${API_URL}/login`, { email, contraseña });
};

export default {
    register,
    login
};
Componentes
Register.js
Define el formulario de registro de usuario.

javascript
Copiar código
import React, { useState } from 'react';
import authService from '../services/authService';

const Register = () => {
    const [nombre, setNombre] = useState('');
    const [email, setEmail] = useState('');
    const [contraseña, setContraseña] = useState('');
    const [carrera, setCarrera] = useState('');
    const [añoDeIngreso, setAñoDeIngreso] = useState('');

    const handleRegister = (e) => {
        e.preventDefault();
        authService.register(nombre, email, contraseña, carrera, añoDeIngreso).then(
            (response) => {
                alert('Usuario registrado con éxito');
            },
            (error) => {
                alert('Error al registrar el usuario');
            }
        );
    };

    return (
        <div>
            <h2>Registro</h2>
            <form onSubmit={handleRegister}>
                <div>
                    <label>Nombre:</label>
                    <input type="text" value={nombre} onChange={(e) => setNombre(e.target.value)} />
                </div>
                <div>
                    <label>Email:</label>
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
                <div>
                    <label>Contraseña:</label>
                    <input type="password" value={contraseña} onChange={(e) => setContraseña(e.target.value)} />
                </div>
                <div>
                    <label>Carrera:</label>
                    <input type="text" value={carrera} onChange={(e) => setCarrera(e.target.value)} />
                </div>
                <div>
                    <label>Año de Ingreso:</label>
                    <input type="number" value={añoDeIngreso} onChange={(e) => setAñoDeIngreso(e.target.value)} />
                </div>
                <button type="submit">Registrar</button>
            </form>
        </div>
    );
};

export default Register;
Pruebas
Realiza pruebas de los endpoints usando Postman o herramientas similares para asegurarte de que el backend responde correctamente. Además, realiza pruebas manuales del frontend para verificar que la interfaz de usuario funcione como se espera.

Despliegue
Backend
Construir la imagen Docker:

bash
Copiar código
docker build -t backend:latest .
Ejecutar el contenedor:

bash
Copiar código
docker run -d -p 5000:5000 backend:latest
Frontend
Construir la aplicación para producción:

bash
Copiar código
npm run build
Servir los archivos estáticos:
Sube los archivos en la carpeta build a un servidor web como Nginx, Apache, o un servicio de alojamiento de sitios estáticos como Vercel o Netlify.

Este manual proporciona una guía completa para configurar y ejecutar el proyecto de registro de usuarios tanto en el entorno de desarrollo como en producción. Asegúrate de personalizar las configuraciones y scripts según las necesidades específicas de tu proyecto.







