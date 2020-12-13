# Generated by Django 3.0.7 on 2020-12-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20201206_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted'), ('morning', 'morning'), ('deleted_by_admin', 'deleted by admin')], default='publish', max_length=25),
        ),
    ]