# Generated by Django 4.1.3 on 2023-01-02 06:45

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_home_brand_image_alter_home_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='favicon',
            field=models.ImageField(default='home/favicon.png', upload_to=core.models.custom_upload_to, verbose_name='Favicon'),
        ),
    ]
