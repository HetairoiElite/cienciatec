from django.db import models
from apps.events.events import Event
from django.core.exceptions import ValidationError

# Create your models here.


class RefereeAssignment(Event):
    publication = models.OneToOneField(
        'events.Publication', on_delete=models.CASCADE, related_name='reviewer_assignment')

    class Meta:
        verbose_name = 'Asignación de revisores'
        verbose_name_plural = 'Asignación de revisores'

    # * comprobar que la fecha de inicio de la asignación de revisores este
    # * dentro del rango de la publicación

    def clean(self):
        if not self.publication.check_overlap(self.start_date, self.end_date):
            raise ValidationError(
                'La fecha de inicio de la asignación de revisores debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Asignación de revisores de la publicación #' + str(self.publication.numero_publicacion)

# * modelo asignación de arbitros


class Assignment(models.Model):
    referee_assignment = models.ForeignKey(
        'reviewer_assignment.RefereeAssignment', on_delete=models.CASCADE, related_name='assignments')
    referees = models.ManyToManyField(
        'registration.Profile', related_name='assignments', blank=True, verbose_name='arbitros')
    article = models.OneToOneField(
        'proposal_reception.ArticleProposal', on_delete=models.CASCADE, related_name='assignments')

    class Meta:
        verbose_name = 'Asignación'
        verbose_name_plural = 'Asignaciones'

    def __str__(self):
        return 'Asignación al artículo ' + str(self.article)

# * perfil de articulo


class Profile(models.Model):
    profile = models.CharField(max_length=100, unique=True, verbose_name='Perfil')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return self.profile


class ArticleProfile(models.Model):
    referee_assignment = models.ForeignKey(
        'reviewer_assignment.RefereeAssignment', on_delete=models.CASCADE, related_name='profile', verbose_name="Asignación de arbitros")
    
    article = models.OneToOneField(
        'proposal_reception.ArticleProposal', on_delete=models.CASCADE, related_name='profile', verbose_name="Artículo")

    profiles = models.ManyToManyField(
        'reviewer_assignment.Profile', related_name='articles', verbose_name='Perfiles')

    class Meta:
        verbose_name = 'Perfil de artículo'
        verbose_name_plural = 'Perfiles de artículo'

    def __str__(self):
        return 'Perfil de artículo de ' + str(self.article)
