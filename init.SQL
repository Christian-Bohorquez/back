-- Crear la base de datos
CREATE DATABASE alumniug;

-- Conectarse a la base de datos
\c alumniug;

-- Crear tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    contraseña_hash VARCHAR(120) NOT NULL,
    carrera VARCHAR(120),
    año_de_ingreso INT
);

-- Crear tabla de publicaciones
CREATE TABLE publicaciones (
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuarios(id) NOT NULL,
    contenido TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Crear tabla de comentarios
CREATE TABLE comentarios (
    id SERIAL PRIMARY KEY,
    publicacion_id INT REFERENCES publicaciones(id) NOT NULL,
    usuario_id INT REFERENCES usuarios(id) NOT NULL,
    contenido TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Crear tabla de amigos
CREATE TABLE amigos (
    id SERIAL PRIMARY KEY,
    usuario_id_1 INT REFERENCES usuarios(id) NOT NULL,
    usuario_id_2 INT REFERENCES usuarios(id) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    UNIQUE (usuario_id_1, usuario_id_2)
);
