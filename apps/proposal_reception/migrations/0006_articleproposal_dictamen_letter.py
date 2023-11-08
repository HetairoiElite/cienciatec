# Generated by Django 4.1.7 on 2023-09-22 11:29

import apps.proposal_reception.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recepcion_Propuestas', '0005_alter_articleproposal_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleproposal',
            name='dictamen_letter',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=apps.proposal_reception.models.custom_upload_to_dictamen_letter, verbose_name='Carta de dictamen'),
        ),
    ]
