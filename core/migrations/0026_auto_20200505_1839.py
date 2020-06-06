# Generated by Django 2.2.10 on 2020-05-05 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20200505_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='report',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='title',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='titlefollow',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='userfollow',
            name='is_deleted',
        ),
        migrations.AlterField(
            model_name='category',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='title',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='titlefollow',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
        migrations.AlterField(
            model_name='userfollow',
            name='status',
            field=models.CharField(choices=[('draft', 'draft'), ('publish', 'publish'), ('deleted', 'deleted')], default='publish', max_length=25),
        ),
    ]