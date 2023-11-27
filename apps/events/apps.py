from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.events'
    label = 'Eventos'
    verbose_name = 'Registro de publicaciones'
