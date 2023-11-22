from django.db import models
from django.contrib.sites.shortcuts import get_current_site
# * TimeStampedModel
from model_utils.models import TimeStampedModel
from apps.reviewer_assignment.managers import AssignmentManager


class Assignment(TimeStampedModel):
    
    objects = AssignmentManager()
    
    publication = models.ForeignKey(
        'Eventos.Publication', on_delete=models.CASCADE, related_name='assignments',
        verbose_name='Publicación')

    referees = models.ManyToManyField(
        'registration.Profile', related_name='assignments', verbose_name='arbitros')
    article = models.OneToOneField(
        'Recepcion_Propuestas.ArticleProposal',
        verbose_name='Artículo',
        on_delete=models.CASCADE, related_name='assignment')

    STATUS_CHOICES = (
        ('1', 'Pendiente'),
        ('2', 'Asignado'),
        ('3', 'En revisión'),
        
        ('4', 'Enviado'),
        
        ('5', 'En recepción'),
        ('6', 'En Dictamen'),
        ('7', 'Completado')
    )

    status = models.CharField(verbose_name='Estatus',
                              max_length=1, choices=STATUS_CHOICES, default='1')

    

    completed = models.BooleanField(verbose_name='Completado', default=False)

    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'

    def __str__(self):
        return str(self.article)
    





class Profile(models.Model):
    profile = models.CharField(
        max_length=100, unique=True, verbose_name='Perfil')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.profile


