import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Корневая папка проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ берём из .env — не храним в коде!
SECRET_KEY = os.getenv('SECRET_KEY')

# В продакшене будет False
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Доверенные хосты из .env
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# ============================
# Приложения
# ============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние библиотеки
    'rest_framework',          # DRF
    'rest_framework_simplejwt', # JWT авторизация
    'corsheaders',             # CORS
    'drf_spectacular',         # OpenAPI документация

    # Наши приложения
    'users',
    'documents',
]

# ============================
# Middleware
# ============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS — должен быть выше CommonMiddleware!
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ============================
# База данных — PostgreSQL
# ============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# ============================
# Пароли
# ============================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================
# Локализация
# ============================
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ============================
# Статика и медиа
# ============================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# Сюда будут загружаться документы пользователей
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================
# DRF настройки
# ============================
REST_FRAMEWORK = {
    # Только авторизованные пользователи имеют доступ по умолчанию
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # JWT как метод авторизации
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Подключаем drf-spectacular для документации
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ============================
# CORS — кто может обращаться к API
# ============================
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Например, React фронтенд
    'http://localhost:8000',
]

# ============================
# OpenAPI документация
# ============================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Document Service API',
    'DESCRIPTION': 'Сервис обработки загружаемых документов',
    'VERSION': '1.0.0',
}
# Говорим Django использовать нашу модель, а не стандартную
AUTH_USER_MODEL = 'users.User'
