# Generated by Django 3.0.7 on 2020-12-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20201215_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='is_entry',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='block',
            name='is_message',
            field=models.BooleanField(default=True),
        ),
    ]