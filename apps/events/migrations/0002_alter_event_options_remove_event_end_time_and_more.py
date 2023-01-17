# Generated by Django 4.1.3 on 2023-01-10 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'Evento', 'verbose_name_plural': 'Eventos'},
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_time',
        ),
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=None, help_text='Fecha de Finalizacion', verbose_name='Fecha de Finalizacion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=None, help_text='Fecha de Inicio', verbose_name='Fecha de Inicio'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.DateField(help_text='Dia del Evento', verbose_name='Dia del Evento'),
        ),
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.TextField(help_text='Notas', verbose_name='Notas'),
        ),
    ]