# Generated by Django 3.1.2 on 2020-12-17 20:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend_site', '0004_auto_20201217_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app_user',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 20, 31, 4, 325197)),
        ),
        migrations.AlterField(
            model_name='suspect_person_detail',
            name='entry_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 17, 20, 31, 4, 324118)),
        ),
        migrations.CreateModel(
            name='suspect_from_app_User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('video_url', models.URLField()),
                ('report_date', models.DateTimeField(default=datetime.datetime(2020, 12, 17, 20, 31, 4, 325860))),
                ('status', models.IntegerField(default=0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend_site.app_user')),
            ],
        ),
    ]