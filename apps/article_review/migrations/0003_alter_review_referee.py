# Generated by Django 4.1.5 on 2023-03-14 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
        ('Revision_Articulo', '0002_review_enviado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='referee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='registration.profile', verbose_name='Arbitro'),
        ),
    ]