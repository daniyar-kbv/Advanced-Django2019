# Generated by Django 2.2.5 on 2019-11-05 18:48

from django.db import migrations, models
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20191001_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcomment',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='taskdocument',
            name='document',
            field=models.FileField(upload_to=utils.upload.task_document_path, validators=[utils.validators.validate_file_size, utils.validators.validate_extension]),
        ),
    ]