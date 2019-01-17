from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.dispatch import receiver
from datetime import timedelta, datetime, date

from django.contrib.auth.models import AbstractUser


def get_age(birth_date: date):
    t2 = datetime.now()
    t1 = birth_date
    if isinstance(t1, date):
        t_year = (t2.year - t1.year)
        t_month = (t2.month - t1.month)
        t_day = (t2.day - t1.day)
        if t_month < 0 or t_day < 0:
            return t_year - 1
        return t_year
    # else:
    #     return 1


class Customer(AbstractUser):
    _avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    activation_key = models.CharField(
        max_length=128,
        blank=True,
        null=True,
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

    @property
    def age(self):
        t2 = datetime.now()
        t1 = self.birth_date
        if isinstance(t1, date):
            t_year = (t2.year - t1.year)
            t_month = (t2.month - t1.month)
            t_day = (t2.day - t1.day)
            if t_month < 0 or t_day < 0:
                return t_year - 1
            return t_year

    def __str__(self):
        return self.username


class CustomerProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER = ((MALE, 'male'), (FEMALE, 'female'))

    customer = models.OneToOneField(
        Customer,
        unique=True,
        on_delete=models.CASCADE,
        null=False,
    )

    _age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    aboutMe = models.TextField(
        max_length=512,
        blank=True,
    )

    gender = models.CharField(
        max_length=6,
        choices=GENDER,
        blank=True,
        # default='NotSet',
    )

    @property
    def age(self):
        if self.customer.birth_date:
            self._age = get_age(self.customer.birth_date)
            self.save()
            return self._age

    @receiver(post_save, sender=Customer)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = CustomerProfile.objects.create(customer=instance)
            new_profile._age = get_age(new_profile.customer.birth_date)

    @receiver(post_save, sender=Customer)
    def save_profile(sender, instance, **kwargs):
        instance.customerprofile.save()

    def __str__(self):
        return self.customer.username
