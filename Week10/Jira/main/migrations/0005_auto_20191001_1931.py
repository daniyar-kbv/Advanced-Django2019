# Generated by Django 2.2.5 on 2019-10-01 19:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20191001_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcomment',
            name='created_at',
            field=models.CharField(default=datetime.datetime(2019, 10, 1, 19, 31, 11, 629046), max_length=100),
        ),
    ]
