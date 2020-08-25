# Generated by Django 2.2.13 on 2020-08-25 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20200814_1005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted'), ('morning', 'morning')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='titlefollow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL),
        ),
    ]