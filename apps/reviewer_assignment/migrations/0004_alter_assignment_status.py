# Generated by Django 4.1.7 on 2023-03-28 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Asignacion_Arbitros', '0003_alter_assignment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.CharField(choices=[('1', 'Pendiente'), ('2', 'Asignado'), ('3', 'En revisión'), ('4', 'Enviado'), ('5', 'En recepción'), ('6', 'En Dictamen')], default='1', max_length=1, verbose_name='Estatus'),
        ),
    ]
