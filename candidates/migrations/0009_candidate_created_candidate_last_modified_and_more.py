# Generated by Django 4.0.4 on 2022-04-28 09:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0008_candidate_work_time_restrictions'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='comments',
            field=models.TextField(blank=True, null=True, verbose_name='Comments'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='work_willing_to_consider',
            field=models.TextField(blank=True, null=True, verbose_name='Types of work you are willing to consider'),
        ),
    ]
