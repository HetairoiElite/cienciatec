from django.db import models
from datetime import datetime

class Event(models.Model):
    title = models.CharField(
        max_length=100, verbose_name='Titulo', help_text='Titulo', default='Nuevo envento')

    start_date = models.DateTimeField(
        verbose_name='Fecha de Inicio', help_text='Fecha de Inicio')
    end_date = models.DateTimeField(
        verbose_name='Fecha de Finalizacion', help_text='Fecha de Finalizacion')
    # notes = models.TextField(verbose_name='Notas',
    #                          help_text='Notas', blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class EventDay(models.Model):
    day = models.DateField(verbose_name='Dia', help_text='Dia')
    start_time = models.TimeField(
        verbose_name='Hora de Inicio', help_text='Hora de Inicio',
        # * 7:00 am
        default=datetime.strptime('07:00', '%H:%M').time()
    )
    end_time = models.TimeField(
        verbose_name='Hora de Finalizacion', help_text='Hora de Finalizacion',
        # * 10:00 pm
        default=datetime.strptime('22:00', '%H:%M').time()
    )

    def __str__(self):
        return str(self.day)

    class Meta:
        abstract = True