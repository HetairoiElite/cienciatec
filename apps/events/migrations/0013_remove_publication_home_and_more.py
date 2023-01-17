# Generated by Django 4.1.3 on 2023-01-15 18:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_alter_articlereview_notes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='home',
        ),
        migrations.AlterField(
            model_name='articlepublication',
            name='end_time',
            field=models.TimeField(default=datetime.time(22, 0), help_text='Hora de Finalizacion', verbose_name='Hora de Finalizacion'),
        ),
        migrations.AlterField(
            model_name='articlepublication',
            name='start_time',
            field=models.TimeField(default=datetime.time(7, 0), help_text='Hora de Inicio', verbose_name='Hora de Inicio'),
        ),
        migrations.AlterField(
            model_name='finalreportsending',
            name='end_time',
            field=models.TimeField(default=datetime.time(22, 0), help_text='Hora de Finalizacion', verbose_name='Hora de Finalizacion'),
        ),
        migrations.AlterField(
            model_name='finalreportsending',
            name='start_time',
            field=models.TimeField(default=datetime.time(7, 0), help_text='Hora de Inicio', verbose_name='Hora de Inicio'),
        ),
    ]