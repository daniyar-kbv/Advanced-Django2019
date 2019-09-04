from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Company(models.Model):
    name = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class ReviewManager(models.Manager):

    def reviews_by_user(self, user):
        return super(ReviewManager, self).get_queryset().filter(reviewer=user)


class Review(models.Model):
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=10000)
    ip_address = models.GenericIPAddressField(protocol='both', default='0.0.0.0')
    submission_date = models.DateField(default=datetime.date.today)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    objects = ReviewManager()

    def __str__(self):
        return self.title

