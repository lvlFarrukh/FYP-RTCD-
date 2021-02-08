# Generated by Django 3.1.5 on 2021-01-24 23:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0019_auto_20201227_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 23, 20, 26, 11682)),
        ),
        migrations.AlterField(
            model_name='caught_suspect',
            name='report_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 23, 20, 26, 14155)),
        ),
        migrations.AlterField(
            model_name='suspect_from_anonymous',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 23, 20, 26, 12948)),
        ),
        migrations.AlterField(
            model_name='suspect_from_app_user',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 23, 20, 26, 12341)),
        ),
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 23, 20, 26, 10743)),
        ),
        migrations.AlterField(
            model_name='suspect_track_list',
            name='recent_track_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 23, 20, 26, 13571, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='suspect_track_list',
            name='report_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 23, 20, 26, 13534, tzinfo=utc)),
        ),
    ]
