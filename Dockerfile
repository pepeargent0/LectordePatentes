FROM ubuntu:latest

# Actualizar el sistema y instalar las dependencias necesarias
RUN apt-get update && apt-get upgrade -y
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx \
    && apt-get install -y tesseract-ocr \
    && apt-get install -y python3-pip \
    && apt-get install -y qtbase5-dev \
    && apt-get install -y qtchooser \
    && apt-get install -y qt5-qmake \
    && apt-get install -y qtbase5-dev-tools

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar tu código Python al contenedor
COPY main.py .

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Configurar las variables de entorno
ENV DISPLAY=:0
ENV LANG=es_MX.UTF-8


# Ejecutar el script Python
CMD ["python3", "main.py"]
