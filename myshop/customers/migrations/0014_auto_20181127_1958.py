# Generated by Django 2.1.1 on 2018-11-27 16:58

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0013_auto_20181127_1942'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerprofile',
            old_name='_age',
            new_name='age',
        ),
        migrations.AlterField(
            model_name='customer',
            name='activation_key_expired',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 29, 16, 57, 50, 640181, tzinfo=utc)),
        ),
    ]