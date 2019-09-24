from django.db import models
from django.contrib.auth.models import AbstractUser


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    bio = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    avatar = models.CharField(max_length=300)
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)