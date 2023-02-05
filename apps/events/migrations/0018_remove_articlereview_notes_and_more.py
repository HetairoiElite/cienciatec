# Generated by Django 4.1.5 on 2023-01-31 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_alter_publication_home'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlereview',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='correctionsreception',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='correctionssending',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='reviewerassignment',
            name='notes',
        ),
        migrations.AlterField(
            model_name='publication',
            name='numero_publicacion',
            field=models.PositiveIntegerField(help_text='Numero de publicación', unique=True, verbose_name='Numero de publicación'),
        ),
    ]