# Generated by Django 3.0.7 on 2021-09-24 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0082_remove_title_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='punish_finish_date',
            field=models.DateField(blank=True, null=True, verbose_name='Punish date'),
        ),
    ]