import os
from pathlib import Path

import extensions.config

# Directories
BASE_DIR = Path(__file__).resolve().parent.parent
PROFILE_DIR = os.path.join(
    os.path.expanduser('~'),
    '.gamedex')
MEDIA = os.path.join(PROFILE_DIR, 'media')

# Import settings from `config.ini`
APP_CFG = extensions.config.cfg['APP']

# Server settings
SECRET_KEY = APP_CFG['key']
if APP_CFG['debug'] == 'True':
    DEBUG = True
else:
    DEBUG = False

# Host settings
ALLOWED_HOSTS = []

if APP_CFG['public_mode']:
    ALLOWED_HOSTS.append('*')
else:
    ALLOWED_HOSTS.append(APP_CFG['server_name'])

# Application definition
INSTALLED_APPS = [
    'library.apps.LibraryConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gamedex.urls'

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

WSGI_APPLICATION = 'gamedex.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': APP_CFG['db'],
    }
}

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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(PROFILE_DIR, 'sys', 'assets')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROFILE_DIR, 'media')

STATICFILES_DIRS = [BASE_DIR / 'assets']
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',  # new
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
