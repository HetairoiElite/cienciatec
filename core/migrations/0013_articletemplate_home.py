# Generated by Django 4.1.5 on 2023-01-20 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_articletemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='articletemplate',
            name='home',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.home', verbose_name='Página principal'),
        ),
    ]