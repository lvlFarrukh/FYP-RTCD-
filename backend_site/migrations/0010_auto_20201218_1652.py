# Generated by Django 3.1.2 on 2020-12-18 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0009_auto_20201218_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 18, 16, 52, 14, 245437)),
        ),
        migrations.AlterField(
            model_name='suspect_from_anonymous',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 18, 16, 52, 14, 246874)),
        ),
        migrations.AlterField(
            model_name='suspect_from_app_user',
            name='report_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 18, 16, 52, 14, 246172)),
        ),
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 18, 16, 52, 14, 244319)),
        ),
    ]