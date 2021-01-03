# Generated by Django 3.1.2 on 2020-12-27 13:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0014_auto_20201227_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 13, 30, 46, 977952)),
        ),
        migrations.AlterField(
            model_name='caught_suspect',
            name='report_date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 13, 30, 46, 979732)),
        ),
        migrations.AlterField(
            model_name='suspect_from_anonymous',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 13, 30, 46, 979219)),
        ),
        migrations.AlterField(
            model_name='suspect_from_app_user',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 13, 30, 46, 978614)),
        ),
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 27, 13, 30, 46, 976848)),
        ),
    ]