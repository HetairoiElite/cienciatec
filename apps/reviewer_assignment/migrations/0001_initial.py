# Generated by Django 4.1.5 on 2023-02-05 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0019_delete_reviewerassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewerAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Nuevo envento', help_text='Titulo', max_length=100, verbose_name='Titulo')),
                ('start_date', models.DateTimeField(help_text='Fecha de Inicio', verbose_name='Fecha de Inicio')),
                ('end_date', models.DateTimeField(help_text='Fecha de Finalizacion', verbose_name='Fecha de Finalizacion')),
                ('publication', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer_assignment', to='events.publication')),
            ],
            options={
                'verbose_name': 'Asignación de revisores',
                'verbose_name_plural': 'Asignación de revisores',
            },
        ),
    ]
