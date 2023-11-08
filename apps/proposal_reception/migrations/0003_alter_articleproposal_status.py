# Generated by Django 4.1.7 on 2023-03-17 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Recepcion_Propuestas', '0002_alter_articleproposal_new_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleproposal',
            name='status',
            field=models.CharField(choices=[('1', 'En espera'), ('2', 'Recibido'), ('3', 'En revisión'), ('4', 'Sin corregir'), ('5', 'Corregido'), ('6', 'Aceptado'), ('7', 'Rechazado')], db_index=True, default='1', max_length=1, verbose_name='Estatus'),
        ),
    ]