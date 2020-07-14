from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Profile model."""

    USER_LEVELS = (
        ('ind', 'Individual'),
        ('pro_dev', 'Property Developer'),
        ('ban_sac', 'Bank/Sacco')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="userprofile", on_delete=models.CASCADE)
    personal_identification = models.CharField(max_length=12, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    image = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=40, choices=USER_LEVELS, default=1)


def __str__(self):
    return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
