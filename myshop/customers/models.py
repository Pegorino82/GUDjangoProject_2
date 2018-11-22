from django.db import models
from django.utils.timezone import now
from datetime import timedelta

from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):
    _avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )

    activation_key = models.CharField(
        max_length=128,
        blank=True
    )

    activation_key_expired = models.DateTimeField(
        default=(now() + timedelta(hours=48))
    )

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expired:
            return False
        else:
            return True

    @property
    def avatar(self):
        if not self._avatar:
            self._avatar = 'avatars/default.jpg'
        return self._avatar

    def __str__(self):
        return self.username
