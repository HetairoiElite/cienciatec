# Generated by Django 4.1.3 on 2023-01-11 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_options_remove_event_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='title',
            field=models.CharField(default='Nuevo envento', help_text='Titulo', max_length=100, verbose_name='Titulo'),
        ),
    ]
