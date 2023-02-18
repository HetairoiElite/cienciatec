from django.apps import AppConfig


class SchoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.school'
    label = 'Escuelas'
    verbose_name = 'Registro de escuelas'