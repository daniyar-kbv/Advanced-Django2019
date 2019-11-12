from django.db import models
from authe.models import MainUser
from main.constants import PROJECT_STATUSES, PROJECT_IN_PROCESS, PROJECT_TYPES, PROJECT_DEVELOPMENT, PROJECT_DONE, \
    PROJECT_FROZEN, PROJECT_OPTIMIZATION
from django.db import models
from utils.upload import document_path as task_document_path
from utils.validators import validate_extension, validate_file_size

import datetime as dt


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(project_type=PROJECT_OPTIMIZATION)

    def optimization_projects(self):
        return self.filter(project_type=PROJECT_OPTIMIZATION)

    def development_projects(self):
        return self.filter(project_type=PROJECT_DEVELOPMENT)

    def filter_by_project_type(self, project_type):
        return self.filter(project_type=project_type)

    def frozen_projects(self):
        return self.filter(status=PROJECT_FROZEN)

    def in_process_projects(self):
        return self.filter(status=PROJECT_IN_PROCESS)

    def done_projects(self):
        return self.filter(status=PROJECT_DONE)

    def filter_by_status(self, status):
        return self.filter(status=status)


class Project(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=False, null=False)
    status = models.PositiveSmallIntegerField(choices=PROJECT_STATUSES, default=PROJECT_IN_PROCESS)
    project_type = models.PositiveSmallIntegerField(choices=PROJECT_TYPES, default=PROJECT_DEVELOPMENT)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    objects = ProjectManager

    def __str__(self):
        return self.name

    # @property
    # def tasks_count(self):
    #     return self.tasks.count()


class Block(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    block_type = models.IntegerField(null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=False, null=False)
    priority = IntegerRangeField(min_value=1, max_value=10, null=False)
    order = models.IntegerField(null=False)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='%(class)s_creator')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='%(class)s_executor', null=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'


class TaskDocument(models.Model):
    document = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension])
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'TaskDocument'
        verbose_name_plural = 'TaskDocuments'


class TaskComment(models.Model):
    body = models.CharField(max_length=300, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)