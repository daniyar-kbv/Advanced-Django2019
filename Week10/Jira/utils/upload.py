from django.conf import settings

import shutil


def folder_name(instance):
    from main.models import TaskDocument
    if type(instance) == TaskDocument:
        return f'{instance.task.id}:{instance.task.name.replace(" ", "_")}'
    return f'{instance.id}:{instance.name.replace(" ", "_")}'


def document_path(instance, filename):
  return f'{instance._meta.verbose_name_plural}/{folder_name(instance)}/{filename}'


def task_document_path(instance, filename):
  return f'tasks/{instance.task.id}:{instance.task.name.replace(" ", "_")}/{filename}'


def avatar_path(instance, filename):
  return f'avatars/{instance.id}/{filename}'


def task_delete_documents(task):
    from main.models import TaskDocument
    task_path = settings.MEDIA_ROOT + f"/{TaskDocument._meta.verbose_name_plural}/{folder_name(task)}/"
    shutil.rmtree(task_path)