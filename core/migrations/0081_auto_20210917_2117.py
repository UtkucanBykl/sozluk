# Generated by Django 3.0.7 on 2021-09-17 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_title_is_deteled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='is_deteled',
            new_name='is_deleted',
        ),
    ]