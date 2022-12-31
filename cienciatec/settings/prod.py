from cienciatec.settings.base import *

# * AWS

# * S3


AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')

AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_DEFAULT_ACL = "public-read"

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_S3_FILE_OVERWRITE = True

AWS_LOCATION = 'static'

AWS_QUERYSTRING_AUTH = False

AWS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATICFILES_STORAGE = 'core.storage_backends.StaticStorage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

PUBLIC_MEDIA_LOCATION = 'media'

DEFAULT_FILE_STORAGE = 'core.storage_backends.PublicMediaStorage'

MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
