# Generated by Django 3.0.7 on 2020-12-15 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0053_auto_20201215_0624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='title',
            field=models.CharField(max_length=400, unique=True),
        ),
    ]
