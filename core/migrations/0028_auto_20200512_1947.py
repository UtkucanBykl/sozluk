# Generated by Django 2.2.10 on 2020-05-12 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_title_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-display_order']},
        ),
        migrations.AddField(
            model_name='category',
            name='display_order',
            field=models.IntegerField(default=0),
        ),
    ]
