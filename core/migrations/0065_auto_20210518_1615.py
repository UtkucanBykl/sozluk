# Generated by Django 3.0.7 on 2021-05-18 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_title_is_ukde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='is_ukde',
            field=models.BooleanField(default=False),
        ),
    ]