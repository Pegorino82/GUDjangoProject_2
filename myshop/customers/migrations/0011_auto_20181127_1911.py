# Generated by Django 2.1.1 on 2018-11-27 16:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0010_auto_20181127_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='activation_key_expired',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 29, 16, 11, 36, 295551, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='customerprofile',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
