from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.publications'
    label = 'Eventos'
    verbose_name = 'Control de publicaciones'
