# Generated by Django 4.1.5 on 2023-02-26 02:55

import apps.proposal_reception.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recepcion_Propuestas', '0003_alter_articleproposal_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='articleproposal',
            name='template_as_pdf',
            field=models.FileField(blank=True, null=True, upload_to=apps.proposal_reception.models.custom_upload_to_template_as_pdf, verbose_name='Plantilla en PDF'),
        ),
    ]