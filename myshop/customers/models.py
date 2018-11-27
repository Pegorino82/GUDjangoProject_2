from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.dispatch import receiver
from datetime import timedelta, datetime

from django.contrib.auth.models import AbstractUser


def get_age(birth_date: datetime):
    t2 = datetime.now()
    t1 = birth_date

    t_year = (t2.year - t1.year)
    t_month = (t2.month - t1.month)
    t_day = (t2.day - t1.day)

    if t_month < 0 or t_day < 0:
        return t_year - 1
    return t_year


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


class CustomerProfile(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        null=True
    )

    age = models.PositiveIntegerField(
        null=True
    )

    @receiver(post_save, sender=Customer)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = CustomerProfile.objects.create(customer=instance)
            new_profile.age = get_age(new_profile.customer.birth_date)

    @receiver(post_save, sender=Customer)
    def save_profile(sender, instance, **kwargs):
        instance.customerprofile.save()
