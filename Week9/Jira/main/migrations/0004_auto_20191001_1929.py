# Generated by Django 2.2.5 on 2019-10-01 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20191001_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcomment',
            name='created_at',
            field=models.CharField(default=datetime.datetime(2019, 10, 1, 19, 29, 25, 490230), max_length=100),
        ),
    ]
