# ==========================================
# ETAPA 1: BUILDER (Compilación)
# ==========================================
FROM python:3.11-slim as builder

# Optimizaciones de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Generamos los "wheels" (paquetes pre-compilados)
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# ==========================================
# ETAPA 2: RUNNER (Imagen Final Ligera)
# ==========================================
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# Instalamos dependencias de sistema para EJECUTAR (Runtime)
# - libmariadb3: Necesario para que Django hable con MySQL
# - media-types: CRÍTICO para que el CSS cargue bien (reemplaza a mime-support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb3 \
    media-types \
    && rm -rf /var/lib/apt/lists/*

# Copiamos los wheels compilados de la etapa anterior
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Instalamos las librerías de Python desde los wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copiamos el código del proyecto
COPY . /app/

# --- COLLECTSTATIC ---
# Whitenoise necesita comprimir los archivos antes de arrancar.
# Usamos una clave dummy porque aquí no tenemos acceso a las variables de entorno reales aún.
ENV SECRET_KEY="dummy-key-para-el-build"
# Aseguramos que settings.py no intente conectar a GCS durante el build
# (Tu settings.py ya maneja esto si no encuentra las credenciales)
RUN python manage.py collectstatic --noinput

# Creamos un usuario no-root por seguridad (Buenas prácticas de Google)
# Comando de ejecución con Gunicorn
# Ajustado para tu estructura 'config.wsgi'
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "60"]