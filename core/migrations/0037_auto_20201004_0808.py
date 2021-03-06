# Generated by Django 3.0.6 on 2020-10-04 08:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20201004_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggested',
            name='title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Title'),
        ),
        migrations.AddField(
            model_name='suggested',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggestions', to=settings.AUTH_USER_MODEL),
        ),
    ]
