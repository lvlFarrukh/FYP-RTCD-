# Generated by Django 3.0.5 on 2020-04-26 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0005_suspect_person_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='date_of_birth',
            field=models.DateField(default='2050-01-01'),
        ),
    ]
