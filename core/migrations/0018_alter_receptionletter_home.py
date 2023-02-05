# Generated by Django 4.1.5 on 2023-01-26 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_receptionletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receptionletter',
            name='home',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reception_letters', to='core.home', verbose_name='Página principal'),
        ),
    ]