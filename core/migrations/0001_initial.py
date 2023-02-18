# Generated by Django 4.1.5 on 2023-02-17 16:29

import core.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('subtitle', models.CharField(max_length=100, verbose_name='Subtítulo')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.models.custom_upload_to_image, verbose_name='Imagen Principal')),
                ('brand_image', models.ImageField(blank=True, null=True, upload_to=core.models.custom_upload_to_brand, verbose_name='Imagen de marca')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to=core.models.custom_upload_to_favicon, verbose_name='Favicon')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('convocatoria', models.FileField(blank=True, null=True, upload_to=core.models.custom_upload_to_convocatoria, verbose_name='Convocatoria')),
                ('acept_template', models.FileField(blank=True, null=True, upload_to=core.models.custom_upload_to_acept_template, verbose_name='Plantilla de aceptación')),
                ('reject_template', models.FileField(blank=True, null=True, upload_to=core.models.custom_upload_to_reject_template, verbose_name='Plantilla de no aceptación')),
            ],
            options={
                'verbose_name': 'Página principal',
                'verbose_name_plural': 'Página principal',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ReceptionLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('template', models.FileField(blank=True, null=True, upload_to=core.models.custom_upload_template_reception_letter, verbose_name='Plantilla')),
                ('current_number', models.PositiveIntegerField(default=1, verbose_name='Número de oficio actual')),
                ('president', models.CharField(max_length=100, verbose_name='Presidente del comité de arbitraje')),
                ('president_firm', models.ImageField(blank=True, null=True, upload_to=core.models.custom_upload_firm_pre, verbose_name='Firma del presidente')),
                ('secretary', models.CharField(max_length=100, verbose_name='Secretario del comité de arbitraje')),
                ('secretary_firm', models.ImageField(blank=True, null=True, upload_to=core.models.custom_upload_firm_sec, verbose_name='Firma del secretario')),
                ('seal', models.ImageField(blank=True, null=True, upload_to=core.models.custom_upload_seal, verbose_name='Sello del departamento de investigación')),
                ('home', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reception_letters', to='Home.home', verbose_name='Página principal')),
            ],
            options={
                'verbose_name': 'Carta de recepción',
                'verbose_name_plural': 'Cartas de recepción',
            },
        ),
        migrations.CreateModel(
            name='ArticleTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('template', models.FileField(blank=True, null=True, upload_to=core.models.custom_upload_to_article_template, verbose_name='Plantilla')),
                ('home', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='article_templates', to='Home.home', verbose_name='Página principal')),
            ],
            options={
                'verbose_name': 'Plantilla de artículo',
                'verbose_name_plural': 'Plantillas de artículos',
                'ordering': ['name'],
            },
        ),
    ]
