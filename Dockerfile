
# Usar una imagen base de Python
FROM python:3.7.8-slim

# Exponer el puerto en el que la aplicación se ejecutará
EXPOSE 8080

# Actualizar pip a la última versión
RUN pip install -U pip

# Copiar el archivo de requerimientos primero para aprovechar el caché de Docker
COPY requirements.txt /requirements.txt

# Instalar los paquetes requeridos
RUN pip install -r /requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . /app

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Definir el comando para ejecutar la aplicación
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
