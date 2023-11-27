from django.db import models
from model_utils.models import TimeStampedModel
from .managers import ReviewManager
# Create your models here.


# * revisión de articulos

# * El arbitro agrega notas y comentarios a la revisión de un articulo.
# * Las notas son booleanas y los comentarios son de texto libre.


class Note(TimeStampedModel):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='notes',
        verbose_name='Arbitraje'
    )
    line = models.PositiveIntegerField(verbose_name='Línea')
    description = models.CharField(max_length=255, verbose_name='Descripción')
    value = models.BooleanField(verbose_name='Corregido', default=False)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return self.description


class Review(TimeStampedModel):
    referee = models.ForeignKey(
        'registration.Profile', on_delete=models.CASCADE, related_name='review', verbose_name='Arbitro'
    )
    assignment = models.ForeignKey(
        'Asignacion_Arbitros.Assignment', on_delete=models.CASCADE, related_name='reviews', verbose_name='Asignación'
    )

    comments = models.TextField(
        verbose_name='Comentarios', blank=True, null=True)

    enviado = models.BooleanField(verbose_name='Enviado', default=False)

    DICTAMENTO_CHOICES = (
        ('1', 'Aceptado'),
        ('2', 'Rechazado'),
    )

    dictamen = models.CharField(
        verbose_name='Dictamen', max_length=1, choices=DICTAMENTO_CHOICES, null=True, blank=True)

    objects = ReviewManager()

    class Meta:
        verbose_name = 'Arbitraje'
        verbose_name_plural = 'Arbitrajes'

    def __str__(self):
        if self.id % 2 == 0:
            return 'Arbitraje #2'
        else:
            return 'Arbitraje #1'
        
