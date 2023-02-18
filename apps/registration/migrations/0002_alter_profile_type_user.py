# Generated by Django 4.1.5 on 2023-02-18 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type_user',
            field=models.CharField(blank=True, choices=[('1', 'Autor'), ('2', 'Evaluador')], max_length=1, null=True, verbose_name='Tipo de usuario'),
        ),
    ]