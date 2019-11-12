from django.db.models.signals import post_delete
from django.dispatch import receiver

from main.models import Task, TaskDocument
from utils.upload import task_delete_documents


@receiver(post_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    if instance:
        task_delete_documents(task=instance)