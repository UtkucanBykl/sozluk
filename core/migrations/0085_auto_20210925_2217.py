# Generated by Django 3.0.7 on 2021-09-25 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0084_punishuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='punishuser',
            old_name='user',
            new_name='punished_user',
        ),
    ]