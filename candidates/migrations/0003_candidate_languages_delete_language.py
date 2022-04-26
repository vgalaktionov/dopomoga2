# Generated by Django 4.0.4 on 2022-04-25 17:30

from django.db import migrations
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_delete_bsnprooffile_delete_cvfile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='languages',
            field=django_jsonform.models.fields.JSONField(default=[{'language': 'uk', 'level': 4}]),
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]