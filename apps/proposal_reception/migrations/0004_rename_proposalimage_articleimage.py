# Generated by Django 4.1.3 on 2023-01-18 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposal_reception', '0003_remove_articleproposal_abstract_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProposalImage',
            new_name='ArticleImage',
        ),
    ]