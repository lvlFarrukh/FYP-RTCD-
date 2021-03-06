# Generated by Django 3.1.2 on 2020-12-17 21:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0006_auto_20201217_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_user',
            name='email',
            field=models.EmailField(default='unknown', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='app_user',
            name='cnic',
            field=models.BigIntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='app_user',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 21, 10, 17, 978913)),
        ),
        migrations.AlterField(
            model_name='suspect_from_app_user',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 21, 10, 17, 980063)),
        ),
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 21, 10, 17, 977350)),
        ),
    ]
