# Generated by Django 3.1.2 on 2020-12-27 12:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0013_auto_20201226_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 12, 51, 11, 239800)),
        ),
        migrations.AlterField(
            model_name='caught_suspect',
            name='report_date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 12, 51, 11, 241568)),
        ),
        migrations.AlterField(
            model_name='caught_suspect',
            name='suspect_image',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='suspect_from_anonymous',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 12, 51, 11, 241031)),
        ),
        migrations.AlterField(
            model_name='suspect_from_app_user',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 12, 51, 11, 240443)),
        ),
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 12, 51, 11, 238855)),
        ),
    ]