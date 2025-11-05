FROM python:3.11-slim

# Metadatos
LABEL maintainer="fsroyertp@academia.usbbog.edu.co" description="Contenedor para DeportesDB - ETL y visualizaciones"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# Dependencias de sistema necesarias para matplotlib y procesamiento
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    pkg-config \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la app
WORKDIR ${APP_HOME}

# Copiar requirements e instalar dependencias primero (cache)
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear carpeta de outputs y darle permisos (por si no existe)
RUN mkdir -p Vizualize/output && chown -R root:root ${APP_HOME}

# Exponer puerto para servidor estático opcional
EXPOSE 8000

# Comando por defecto: ejecuta main.py
# Si prefieres sólo levantar un servidor estático usa: ["./serve_outputs.sh"]
CMD ["python", "main.py"]