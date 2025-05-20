# cine_plataforma/settings.py

from pathlib import Path
import os  # Para leer variables de entorno
# import dj_database_url # Descomenta si usas una DB externa como PostgreSQL
# from decouple import config # Descomenta si prefieres usar python-decouple

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CONFIGURACIÓN PARA PRODUCCIÓN Y VARIABLES DE ENTORNO ---

# SECRET_KEY: ¡NUNCA hardcodear en producción! Leer desde variable de entorno.
# El segundo argumento de os.environ.get es un valor por defecto SI la variable no se encuentra.
# Este default SOLO se usará si corres localmente y no has configurado la variable.
# En Vercel, SIEMPRE se usará el valor que pusiste en las Variables de Entorno de Vercel.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-0ffrxr!5f8um_*1s+8v*8j66%wfo^9_uamms$lvjflpx&+=1w!' # Default MUY inseguro, solo para que arranque localmente si no hay .env
)

# DEBUG: Leer desde variable de entorno. Por defecto False para producción.
# En Vercel, establece la variable de entorno DEBUG a 'False' (la cadena).
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS: Leer desde variable de entorno.
# En Vercel, establece la variable ALLOWED_HOSTS como 'tu-dominio.vercel.app,.vercel.app'
ALLOWED_HOSTS_STRING = os.environ.get('ALLOWED_HOSTS', '')
if ALLOWED_HOSTS_STRING:
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STRING.split(',') if host.strip()]
elif DEBUG: # Para desarrollo local si ALLOWED_HOSTS no está en el entorno
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
else: # En producción, si no se define ALLOWED_HOSTS, es un error de configuración
    ALLOWED_HOSTS = []
    # Si quieres que falle ruidosamente en producción si no está configurado:
    # from django.core.exceptions import ImproperlyConfigured
    # if not DEBUG and not ALLOWED_HOSTS_STRING:
    #     raise ImproperlyConfigured("LA VARIABLE DE ENTORNO ALLOWED_HOSTS NO ESTÁ CONFIGURADA PARA PRODUCCIÓN!")

# Elimina esta línea de aquí, no pertenece a settings.py:
# DJANGO_SETTINGS_MODULE = 'cine_plataforma.settings'

# --- FIN DE LA CONFIGURACIÓN PARA PRODUCCIÓN ---


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Para servir estáticos con WhiteNoise en desarrollo si DEBUG=True
    'django.contrib.staticfiles',
    'catalogo',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Posición recomendada: después de SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cine_plataforma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Si tienes una carpeta 'templates' global en la raíz del proyecto
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Útil para el contexto de debug en plantillas
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cine_plataforma.wsgi.application' # Asegúrate que 'cine_plataforma' es el nombre correcto de tu proyecto


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # Sigue usando SQLite localmente
    }
}

# --- (Opcional) Para usar una DB externa en Vercel (como Vercel Postgres) ---
# Descomenta estas líneas y asegúrate de tener 'dj-database-url' en requirements.txt
# DATABASE_URL = os.environ.get('DATABASE_URL')
# if DATABASE_URL:
#     DATABASES['default'] = dj_database_url.config(
#         conn_max_age=600,
#         ssl_require=os.environ.get('DB_SSL_REQUIRE', 'False').lower() == 'true' # Vercel Postgres suele necesitar SSL
#     )


# Password validation
# ... (sin cambios, déjalo como estaba) ...
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# ... (sin cambios, déjalo como estaba) ...
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
# USE_L10N = True # Django 5.x ya no usa esto directamente, usa FORMAT_MODULE_PATH
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/' # Django 5.x prefiere '/static/' con la barra al final

# Directorios adicionales donde Django buscará archivos estáticos
# (además de la carpeta 'static' de cada app).
# Útil si tienes una carpeta 'static' global en la raíz de tu proyecto Django (al mismo nivel que manage.py).
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Directorio donde `python manage.py collectstatic` copiará todos los archivos estáticos para producción.
# WhiteNoise servirá los archivos desde esta carpeta cuando DEBUG = False.
STATIC_ROOT = BASE_DIR / 'staticfiles' # Usar Pathlib es más moderno

# Almacenamiento para WhiteNoise, maneja compresión y cacheo eficiente.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Elimina la segunda definición de STATIC_ROOT, ya está arriba.


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'