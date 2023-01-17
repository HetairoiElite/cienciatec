from django.db import models
from django.core.exceptions import ValidationError

# * django models utils
from model_utils.models import TimeStampedModel

from apps.events.events import Event

# Create your models here.
class ProposalReception(Event):

    publication = models.OneToOneField(
        'events.Publication', on_delete=models.CASCADE, related_name='proposal_reception', verbose_name='Publicación')

    class Meta:
        verbose_name = 'Recepción de propuestas'
        verbose_name_plural = 'Recepción de propuestas'

    # * comprobar que la fecha de inicio de la recepción este
    # * dentro del rango de la publicación

    def clean(self):
        if not self.publication.check_overlap(self.start_date, self.end_date):
            raise ValidationError(
                'La fecha de inicio de la recepción de propuestas debe estar dentro del rango de la publicación')

        super().clean()

    def __str__(self):
        return 'Recepción de propuestas de la publicación #' + str(self.publication.numero_publicacion)
    

class ArticleProposal(TimeStampedModel):
    proposal_reception = models.ForeignKey(
        ProposalReception, on_delete=models.CASCADE, related_name='article_proposals', verbose_name='Recepción de propuestas')
    title = models.CharField(
        max_length=100, verbose_name='Titulo', help_text='Titulo', default='Nuevo envento')
    author = models.CharField(
        max_length=100, verbose_name='Autor', help_text='Autor', default='Nuevo envento')
    email = models.EmailField(
        max_length=100, verbose_name='Correo', help_text='Correo', default='Nuevo envento')
    abstract = models.TextField(
        max_length=100, verbose_name='Resumen', help_text='Resumen', default='Nuevo envento')
    keywords = models.TextField(
        max_length=100, verbose_name='Palabras clave', help_text='Palabras clave', default='Nuevo envento')
    file = models.FileField(
        upload_to='article_proposals', verbose_name='Archivo', help_text='Archivo', default='Nuevo envento')

    class Meta:
        verbose_name = 'Propuesta de artículo'
        verbose_name_plural = 'Propuestas de artículos'

    def __str__(self):
        return self.title
