from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Homes(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, related_name="owner", on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    size = models.CharField(max_length=30, blank=True)
    price = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name
