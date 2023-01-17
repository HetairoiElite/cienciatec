# Generated by Django 4.1.3 on 2023-01-15 20:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_school_options_alter_school_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='school',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator('^([a-zA-ZñÑáéíóúÁÉÍÓÚ])*(\\s([a-zA-ZñÑáéíóúÁÉÍÓÚ])*)*$', 'Solo se permiten letras')], verbose_name='País'),
        ),
        migrations.AlterField(
            model_name='school',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator('^([a-zA-ZñÑáéíóúÁÉÍÓÚ])*(\\s([a-zA-ZñÑáéíóúÁÉÍÓÚ])*)*$', 'Solo se permiten letras')], verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='school',
            name='zip_code',
            field=models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{5}$', 'Solo se permiten 5 números')], verbose_name='Código postal'),
        ),
    ]
