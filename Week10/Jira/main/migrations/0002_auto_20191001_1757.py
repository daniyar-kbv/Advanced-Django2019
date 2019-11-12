# Generated by Django 2.2.5 on 2019-10-01 17:57

import datetime
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'DEVELOPMENT'), (2, 'OPTIMIZATION')], default=1),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'DONE'), (2, 'IN_PROCESS'), (3, 'FROZEN')], default=2),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=main.models.IntegerRangeField(),
        ),
        migrations.AlterField(
            model_name='taskcomment',
            name='created_at',
            field=models.CharField(default=datetime.datetime(2019, 10, 1, 17, 57, 29, 983640), max_length=100),
        ),
    ]