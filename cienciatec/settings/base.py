"""
Django settings for cienciatec project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import django
from django.utils.encoding import smart_str
django.utils.encoding.smart_text = smart_str

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1',os.getenv('IP_HOST'), os.getenv('LOCAL_IP')]

# Daphne
# ASGI_APPLICATION = "cienciatec.asgi.application"
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

THIRD_PARTY_APPS = [
    'imagefield',
    'jet.dashboard',
    'jet',
    # 'daphne',
    'storages',
    'corsheaders'
]

LOCAL_APPS = [
    # 'apps.chat',
    'apps.registration',
    'core',
    'apps.school',
    'apps.core_dashboard',
    'apps.publications',
    'apps.proposal_reception',
    'apps.reviewer_assignment',
    'apps.article_review',
    'apps.correction_reception',
    'apps.final_report_sending',
]

INSTALLED_APPS = THIRD_PARTY_APPS + LOCAL_APPS +  DJANGO_APPS



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'cienciatec.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.home',
            ],
        },
    },
]

WSGI_APPLICATION = 'cienciatec.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True




# * Logout
LOGOUT_REDIRECT_URL = 'home'

# * Login
LOGIN_REDIRECT_URL = 'home'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# * Reset Password Email Token Expiration Time

PASSWORD_RESET_TIMEOUT = 3600  # 1 hour

# * SESSION DURATION

SESSION_COOKIE_AGE = 3600 * 2  # 2 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

# # * Celery

# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'django-db'
# DEBUG=True

# * JET

JET_MODULE_GOOGLE_ANALYTICS_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'client_secrets.json')

# JET_INDEX_DASHBOARD = 'cienciatec.urls.CustomIndexDashboard'

JET_INDEX_DASHBOARD = 'cienciatec.urls.CustomIndexDashboard'