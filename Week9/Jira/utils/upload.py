def task_document_path(instance, filename):
  return f'tasks/{instance.id}_{instance.task.name}/{filename}'


def avatar_path(instance, filename):
  return f'avatars/{instance.id}/{filename}'