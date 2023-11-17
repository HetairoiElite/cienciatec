# Generated by Django 4.1.7 on 2023-11-16 20:50

import apps.proposal_reception.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recepcion_Propuestas', '0007_articleproposal_rights_transfer_letter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleproposal',
            name='rights_transfer_letter',
            field=models.FileField(null=True, upload_to=apps.proposal_reception.models.custom_upload_to_rights_transfer_letter, verbose_name='Carta de cesión de derechos'),
        ),
    ]
