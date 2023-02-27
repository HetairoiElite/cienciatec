from django.db import models
from model_utils.models import TimeStampedModel
# Create your models here.


# * revisión de articulos

# * El arbitro agrega notas y comentarios a la revisión de un articulo.
# * Las notas son booleanas y los comentarios son de texto libre.


class Note(models.Model):
    review = models.ForeignKey(
        'Review', on_delete=models.CASCADE, related_name='notes',
        verbose_name='Revisión'
    )
    line = models.PositiveIntegerField(verbose_name='Línea')
    description = models.CharField(max_length=100, verbose_name='Descripción')
    value = models.BooleanField(verbose_name='Corregido')

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return self.description


class Review(TimeStampedModel):
    assignment = models.OneToOneField(
        'Asignacion_Arbitros.Assignment', on_delete=models.CASCADE, related_name='review', verbose_name='Asignación'
    )

    comments = models.TextField(verbose_name='Comentarios', blank=True, null=True)

    class Meta:
        verbose_name = 'Revisión'
        verbose_name_plural = 'Revisiones'

    def __str__(self):
        return str(self.assignment.article)
