from django.db import models
from core import validators
from .managers import SchoolManager
from model_utils.models import TimeStampedModel
# Create your models here.


class School(TimeStampedModel):
    name = models.CharField(
        max_length=100, verbose_name='Nombre', validators=[validators.name])

    is_external = models.BooleanField(default=False, verbose_name='Externo')

    objects = SchoolManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Escuela'
