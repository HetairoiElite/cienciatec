from cienciatec.settings.base import *


# * Storage
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')

# AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')

# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# AWS_DEFAULT_ACL = "public-read"

# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }

# AWS_S3_FILE_OVERWRITE = True

# AWS_LOCATION = 'static'

# AWS_QUERYSTRING_AUTH = False

# AWS_HEADERS = {
#     "Access-Control-Allow-Origin": "*",
# }

# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/4.1/howto/static-files/


# STATICFILES_STORAGE = 'core.storage_backends.StaticStorage'

# STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# PUBLIC_MEDIA_LOCATION = 'media'

# DEFAULT_FILE_STORAGE = 'core.storage_backends.PublicMediaStorage'

# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# * cors


ALLOWED_HOSTS=['*']

CORS_ORIGIN_ALLOW_ALL = True

SECURE_CROSS_ORIGIN_OPENER_POLICY = None

MIDDLEWARE.append('corsheaders.middleware.CorsMiddleware',)

# * Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# * Email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')