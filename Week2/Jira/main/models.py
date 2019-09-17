from django.db import models
from authe.models import MainUser

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    status = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)

class Block(models.Model):
    name = models.CharField(max_length=100)
    block_type = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    priority = models.CharField(max_length=100)
    order = models.IntegerField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='%(class)s_creator')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='%(class)s_executor')
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

class TaskDocument(models.Model):
    document = models.CharField(max_length=200)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class TaskComment(models.Model):
    body = models.CharField(max_length=300)
    created_at = models.CharField(max_length=100)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
