# Generated by Django 2.2.5 on 2019-10-01 19:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20191001_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcomment',
            name='created_at',
            field=models.CharField(default=datetime.datetime(2019, 10, 1, 19, 37, 34, 459288), max_length=100),
        ),
    ]
