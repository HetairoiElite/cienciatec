# Generated by Django 4.1.5 on 2023-01-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal_reception', '0006_alter_articleimage_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coauthor',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico'),
        ),
    ]
