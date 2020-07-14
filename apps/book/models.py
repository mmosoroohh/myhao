from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from ..homes.models import Homes


class Book(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='developer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    home = models.ForeignKey(
        Homes,
        related_name='booked_home',
        on_delete=models.CASCADE
    )
    amount = models.CharField(max_length=30, null=False)

    class Meta:
        app_label = 'book'

    def __str__(self):
        return self.amount
