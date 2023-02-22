from django.db import models
from apps.events.events import Event
from django.core.exceptions import ValidationError

# Create your models here.


# * modelo asignación de arbitros


class Assignment(models.Model):
    publication = models.OneToOneField(
        'Eventos.Publication', on_delete=models.CASCADE, related_name='assignments',
        verbose_name='Publicación')

    referees = models.ManyToManyField(
        'registration.Profile', related_name='assignments', blank=True, verbose_name='arbitros')
    article = models.OneToOneField(
        'Recepcion_Propuestas.ArticleProposal',
        verbose_name='Artículo',
        on_delete=models.CASCADE, related_name='assignments')

    STATUS_CHOICES = (
        ('P', 'Pendiente'),
        ('A', 'Asignado'),
    )

    status = models.CharField(verbose_name='Estatus', max_length=1, choices=STATUS_CHOICES, default='P')
        
    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'

    def __str__(self):
        return 'Asignación al artículo ' + str(self.article)

# * perfil de articulo


class Profile(models.Model):
    profile = models.CharField(
        max_length=100, unique=True, verbose_name='Perfil')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.profile


class ArticleProfile(models.Model):
    publication = models.OneToOneField(
        'Eventos.Publication', on_delete=models.CASCADE, related_name='article_profiles',
        verbose_name='Publicación')

    article = models.OneToOneField(
        'Recepcion_Propuestas.ArticleProposal', on_delete=models.CASCADE, related_name='profile', verbose_name="Artículo")

    profiles = models.ManyToManyField(
        'Asignacion_Arbitros.Profile', related_name='articles', verbose_name='Perfiles')

    class Meta:
        verbose_name = 'Perfil de artículo'
        verbose_name_plural = 'Perfiles de artículo'

    def __str__(self):
        return 'Perfil de artículo de ' + str(self.article)
