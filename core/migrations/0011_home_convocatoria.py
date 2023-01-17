# Generated by Django 4.1.3 on 2023-01-15 18:07

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_home_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='convocatoria',
            field=models.FileField(blank=True, null=True, upload_to=core.models.custom_upload_to, verbose_name='Convocatoria'),
        ),
    ]
