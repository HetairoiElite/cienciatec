from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from model_utils.models import TimeStampedModel


class Event(TimeStampedModel):
    # title = models.CharField(
    #     max_length=100, verbose_name='Titulo', help_text='Titulo', default='Nuevo envento')

    start_date = models.DateTimeField(
        verbose_name='Fecha de Inicio', help_text='Fecha de Inicio')
    end_date = models.DateTimeField(
        verbose_name='Fecha de Finalizacion', help_text='Fecha de Finalizacion', null=True, blank=True)
    # notes = models.TextField(verbose_name='Notas',
    #                          help_text='Notas', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date is not None:
            if self.start_date > self.end_date:
                raise ValidationError(
                    'La fecha de inicio no puede ser mayor a la fecha de finalizacion')

