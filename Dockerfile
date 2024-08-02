# Usa una imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y la aplicación al contenedor
COPY requirements.txt requirements.txt
COPY . .
# Copia el archivo .env al contenedor
COPY .env .env
# Instala las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto en el que la aplicación escuchará
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["flask", "run"]
