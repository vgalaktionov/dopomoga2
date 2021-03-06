# Generated by Django 4.0.4 on 2022-04-25 15:11

from django.db import migrations, models
import django_countries.fields
import localflavor.nl.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BSNProofFile',
        ),
        migrations.DeleteModel(
            name='CVFile',
        ),
        migrations.RemoveField(
            model_name='diplomacertificate',
            name='candidate',
        ),
        migrations.DeleteModel(
            name='DiplomaCertificateFile',
        ),
        migrations.DeleteModel(
            name='PassportFile',
        ),
        migrations.AddField(
            model_name='candidate',
            name='diplomas_certificates',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='bsn_proof_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='city',
            field=models.CharField(max_length=200, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='country',
            field=django_countries.fields.CountryField(default='NL', max_length=2, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='date_of_birth',
            field=models.DateField(verbose_name='Date of birth'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='email',
            field=models.EmailField(max_length=200, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Last name'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='marital_status',
            field=models.CharField(choices=[('UNMARRIED', 'Unmarried'), ('MARRIED', 'Married'), ('COHABITANT', 'Cohabitant'), ('DIVORCED', 'Divorced'), ('WIDOWED', 'Widowed'), ('UNKNOWN', 'Unknown')], default='UNMARRIED', max_length=15, verbose_name='Marital status'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='passport_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone number'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='street',
            field=models.CharField(max_length=200, verbose_name='Street'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='street_number',
            field=models.CharField(max_length=10, verbose_name='Street number'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='title',
            field=models.CharField(choices=[('MR', 'Mr.'), ('MS', 'Ms.')], default='MS', max_length=10, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='zipcode',
            field=localflavor.nl.models.NLZipCodeField(max_length=7, verbose_name='Zipcode'),
        ),
        migrations.DeleteModel(
            name='DiplomaCertificate',
        ),
    ]
