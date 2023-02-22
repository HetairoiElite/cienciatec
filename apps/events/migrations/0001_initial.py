# Generated by Django 4.1.5 on 2023-02-21 19:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start_date', models.DateTimeField(help_text='Fecha de Inicio', verbose_name='Fecha de Inicio')),
                ('end_date', models.DateTimeField(blank=True, help_text='Fecha de Finalizacion', null=True, verbose_name='Fecha de Finalizacion')),
                ('numero_publicacion', models.PositiveIntegerField(help_text='Numero de publicación', unique=True, verbose_name='Numero de publicación')),
                ('current', models.BooleanField(default=True, help_text='Publicación actual', verbose_name='Publicación actual')),
                ('home', models.ForeignKey(blank=True, default='1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='Home.home')),
            ],
            options={
                'verbose_name': 'Publicación',
                'verbose_name_plural': 'Publicaciones',
            },
        ),
    ]
