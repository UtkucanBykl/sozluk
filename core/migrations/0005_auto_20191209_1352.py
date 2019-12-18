# Generated by Django 2.2.7 on 2019-12-09 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20191206_1049'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='title',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL),
        ),
    ]
