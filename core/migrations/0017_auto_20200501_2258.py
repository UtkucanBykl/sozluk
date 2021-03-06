# Generated by Django 2.2.10 on 2020-05-01 22:58

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_notification_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='last_vote_Time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 1, 22, 58, 16, 32093, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='title',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
