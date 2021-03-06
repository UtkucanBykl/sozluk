# Generated by Django 2.2.10 on 2020-05-08 20:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_title_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', related_query_name='title', to='core.Category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', related_query_name='title', to=settings.AUTH_USER_MODEL),
        ),
    ]
