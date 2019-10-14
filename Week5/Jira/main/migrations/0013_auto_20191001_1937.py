# Generated by Django 2.2.5 on 2019-10-01 19:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20191001_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskcomment',
            name='task',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Task'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taskcomment',
            name='created_at',
            field=models.CharField(default=datetime.datetime(2019, 10, 1, 19, 37, 19, 367125), max_length=100),
        ),
    ]