# Generated by Django 4.1.7 on 2023-03-27 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Revision_Articulo', '0004_review_dictamen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='dictamen',
            field=models.CharField(blank=True, choices=[('1', 'Aceptado'), ('2', 'Rechazado')], max_length=1, null=True, verbose_name='Dictamen'),
        ),
    ]
