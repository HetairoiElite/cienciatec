# Generated by Django 4.1.5 on 2023-02-05 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_school_address_alter_school_country_and_more'),
        ('proposal_reception', '0018_alter_articleproposal_new_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleproposal',
            name='new_school',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Institución NO normalizada'),
        ),
        migrations.AlterField(
            model_name='articleproposal',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_proposals', to='school.school', verbose_name='Institución de adscripción'),
        ),
    ]
