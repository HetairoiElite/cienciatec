# Generated by Django 4.1.3 on 2023-01-13 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_home_brand_image_alter_home_favicon_and_more'),
        ('events', '0006_alter_publication_options_proposalreception_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='home',
            field=models.ForeignKey(default=2, help_text='Página principal', on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='core.home', verbose_name='Página principal'),
        ),
    ]
