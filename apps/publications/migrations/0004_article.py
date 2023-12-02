# Generated by Django 4.1.7 on 2023-12-02 10:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Recepcion_Propuestas', '0014_remove_articleproposal_doi'),
        ('Eventos', '0003_publication_numero_folio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('file', models.FileField(upload_to='articles/', verbose_name='Archivo')),
                ('fecha_publicacion', models.DateField(blank=True, null=True, verbose_name='Fecha de publicación')),
                ('doi', models.CharField(blank=True, max_length=100, null=True, verbose_name='DOI')),
                ('article_proposal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='Recepcion_Propuestas.articleproposal')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='Eventos.publication')),
            ],
            options={
                'verbose_name': 'Artículo',
                'verbose_name_plural': 'Artículos',
            },
        ),
    ]
