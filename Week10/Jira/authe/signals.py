from django.db.models.signals import post_save
from django.dispatch import receiver

from authe.models import MainUser, Profile


@receiver(post_save, sender=MainUser)
def uer_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)