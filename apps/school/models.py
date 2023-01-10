from django.db import models
from core import validators
from .managers import SchoolManager
# Create your models here.


class School(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='Nombre', validators=[validators.name])
    address = models.CharField(
        max_length=100, verbose_name='Dirección')
    city = models.CharField(
        max_length=100, verbose_name='Ciudad', validators=[validators.name], null=True, blank=True)
    state = models.CharField(
        max_length=100, verbose_name='Estado', validators=[validators.name])
    zip_code = models.CharField(
        max_length=100, verbose_name='Código postal', validators=[validators.zip_code])
    country = models.CharField(
        max_length=100, verbose_name='País', validators=[validators.name])
    phone = models.CharField(
        max_length=100, verbose_name='Teléfono', validators=[validators.phone], null=True, blank=True)
    email = models.EmailField(
        max_length=100, verbose_name='Correo electrónico', null=True, blank=True)
    website = models.CharField(
        max_length=100, verbose_name='Sitio web', validators=[validators.web_address], null=True, blank=True)
    # * boolean external
    is_external = models.BooleanField(default=False, verbose_name='Externo')

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Actualizado en')
    
    objects = SchoolManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Escuela'
