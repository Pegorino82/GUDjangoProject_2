# Generated by Django 2.1.1 on 2018-11-29 16:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0019_auto_20181129_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='activation_key_expired',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 1, 16, 26, 47, 183554, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customerprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'male'), ('F', 'female')], max_length=6),
        ),
    ]