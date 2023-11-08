# Generated by Django 4.1.7 on 2023-03-17 02:31

import apps.correction_reception.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recepcion_Correcciones', '0003_alter_articlecorrection_correction_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlecorrection',
            name='correction_file_as_pdf',
            field=models.FileField(null=True, upload_to=apps.correction_reception.models.custom_upload__to_correction, verbose_name='Plantilla corregida en PDF'),
        ),
    ]
