from django.db import models
from django.conf import settings

class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedback',
        null=True,
        blank=True
    )
    email = models.EmailField()

    text = models.TextField(
        max_length=512
    )

    created = models.DateTimeField(
        auto_now_add=True
    )