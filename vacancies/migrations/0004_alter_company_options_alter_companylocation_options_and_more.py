# Generated by Django 4.0.4 on 2022-05-03 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0003_company_created_company_last_modified_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='companylocation',
            options={'verbose_name_plural': 'Company Locations'},
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name_plural': 'Vacancies'},
        ),
    ]
