from django.db import models


class Image(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True
    )
    img = models.ImageField(
        upload_to='images/'
    )

    def __str__(self):
        return self.name
