# Generated by Django 3.0.7 on 2020-12-06 17:23

import core.utils.upload
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20201205_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(default='', max_length=255, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=255, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=255, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=core.utils.upload.generate_upload_path),
        ),
    ]