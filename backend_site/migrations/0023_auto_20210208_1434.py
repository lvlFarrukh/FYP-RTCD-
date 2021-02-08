# Generated by Django 3.1.5 on 2021-02-08 14:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0022_auto_20210208_1433'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app_user',
            old_name='address',
            new_name='city',
        ),
        migrations.AlterField(
            model_name='app_user',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 14, 34, 7, 933939)),
        ),
        migrations.AlterField(
            model_name='caught_suspect',
            name='report_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 14, 34, 7, 936995)),
        ),
        migrations.AlterField(
            model_name='suspect_from_anonymous',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 14, 34, 7, 935687)),
        ),
        migrations.AlterField(
            model_name='suspect_from_app_user',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 14, 34, 7, 934756)),
        ),
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 14, 34, 7, 932828)),
        ),
        migrations.AlterField(
            model_name='suspect_track_list',
            name='recent_track_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 14, 34, 7, 936312, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='suspect_track_list',
            name='report_date_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 8, 14, 34, 7, 936265, tzinfo=utc)),
        ),
    ]
