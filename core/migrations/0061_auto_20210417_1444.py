# Generated by Django 3.0.7 on 2021-04-17 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_user_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateField(blank=True, null=True, verbose_name='Last login date'),
        ),
    ]
