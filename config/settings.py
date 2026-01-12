"""
Django settings for alquimista project.
"""

from datetime import timedelta
import os
from pathlib import Path
import dj_database_url

# Google Imports para Storage
from google.auth import default, impersonated_credentials
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SEGURIDAD Y HOSTS
# ==============================================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-cambiar-en-produccion")

# DEBUG: Convertir string a booleano seguro
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

DOMINIOS_FIJOS = [
    "127.0.0.1",
    "localhost",
    ".ngrok-free.app",
]
DOMINIOS_EXTRA = os.environ.get("ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = DOMINIOS_FIJOS + [host.strip() for host in DOMINIOS_EXTRA if host.strip()]

# CSRF (Importante para formularios en producción)
CSRF_TRUSTED_ORIGINS = [
    "https://*.run.app",      # Permite dominios de Cloud Run
    "https://*.ngrok-free.app",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
if os.environ.get("DOMAIN_NAME"):
    CSRF_TRUSTED_ORIGINS.append(f"https://{os.environ.get('DOMAIN_NAME')}")

# ==============================================================================
# APLICACIONES
# ==============================================================================
INSTALLED_APPS = [
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "storages",
    "corsheaders",
    
    "core", 
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls" # Asegúrate que tu carpeta de config se llama 'config'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ==============================================================================
# BASE DE DATOS
# ==============================================================================
if "DATABASE_URL" in os.environ:
    DATABASES = {"default": dj_database_url.config(conn_max_age=600, ssl_require=False)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": os.environ.get("DB_HOST"),
            "PORT": os.environ.get("DB_PORT"),
            "CONN_MAX_AGE": 60,
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET default_storage_engine=INNODB",
            },
            # Configuración para tests:
            "TEST": {
                "NAME": None,  # None = Django crea automáticamente test_<nombre_bd>
                "CHARSET": "utf8mb4",
                "COLLATION": "utf8mb4_unicode_ci",
            },
        }
    }

# ==============================================================================
# ALMACENAMIENTO (La parte importante de Parchaoo)
# ==============================================================================


STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


# 2. MEDIA FILES (Imágenes subidas) -> Se sirven con GCS o Local
if DEBUG:
    # --- DESARROLLO LOCAL (Carpetas normales) ---
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
    
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
    
    print("[STORAGE] Modo LOCAL: Archivos se guardan en carpeta 'media/'")
    
else:
    # --- PRODUCCIÓN (Google Cloud Storage) ---
    GS_BUCKET_NAME = os.environ.get("GS_BUCKET_NAME")
    GS_PROJECT_ID = os.environ.get("GS_PROJECT_ID", "alquimista")
    GS_DEFAULT_ACL = None
    GS_FILE_OVERWRITE = False
    GS_SERVICE_ACCOUNT_EMAIL = os.environ.get("GS_SERVICE_ACCOUNT_EMAIL")
    
    # Configurar credenciales de GCS
    try:
        source_credentials, project_id = default()
        target_service_account = GS_SERVICE_ACCOUNT_EMAIL
        
        if target_service_account:
            GS_CREDENTIALS = impersonated_credentials.Credentials(
                source_credentials=source_credentials,
                target_principal=target_service_account,
                target_scopes=["https://www.googleapis.com/auth/devstorage.full_control"],
                lifetime=3600,
            )
            print(f"[GCS] Credenciales Impersonadas activas para: {target_service_account}")
        else:
            # Si no hay target_service_account, usar credenciales directas
            GS_CREDENTIALS = source_credentials
            print("[GCS] Usando credenciales por defecto de Google Cloud")
    except Exception as e:
        print(f"[GCS] Aviso: No se detectaron credenciales de GCP ({e}).")
        print("   -> Esto es normal durante el 'docker build'.")
        GS_CREDENTIALS = None
    
    # Configuración de MEDIA para producción (GCS)
    if GS_CREDENTIALS is not None and GS_BUCKET_NAME:
        MEDIA_ROOT = ""
        MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"
        
        STORAGES = {
            # Almacenamiento por defecto (archivos públicos/productos)
            "default": {
                "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
                "OPTIONS": {
                    "bucket_name": GS_BUCKET_NAME,
                    "querystring_auth": True,
                    "expiration": timedelta(seconds=300),
                    "project_id": GS_PROJECT_ID,
                    "default_acl": GS_DEFAULT_ACL,
                    "file_overwrite": GS_FILE_OVERWRITE,
                    "credentials": GS_CREDENTIALS,
                },
            },
            # Archivos estáticos
            "staticfiles": {
                "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
            },
        }
        
        print("[STORAGE] Modo PRODUCCION: Archivos se guardan en Google Cloud Storage")
    else:
        # Fallback si no hay credenciales o bucket configurado
        MEDIA_ROOT = BASE_DIR / "media"
        MEDIA_URL = "/media/"
        STORAGES = {
            "default": {
                "BACKEND": "django.core.files.storage.FileSystemStorage",
            },
            "staticfiles": {
                "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
            },
        }
        print("[STORAGE] Fallback a sistema local: No hay configuracion de GCS valida")

# ==============================================================================
# LOGGING (Optimizado para Cloud Run igual que Parchaoo)
# ==============================================================================
IS_CLOUD_RUN = os.environ.get("K_SERVICE") is not None

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} | {module} | {message}",
            "style": "{",
        },
        "cloud_run": {
            # Formato simple para que Cloud Logging lo parsee bien
            "format": "[{name}] [{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "cloud_run" if IS_CLOUD_RUN else "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Configuración Regional
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'