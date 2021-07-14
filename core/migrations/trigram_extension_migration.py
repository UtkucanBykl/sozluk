from django.db import migrations
from django.contrib.postgres.operations import UnaccentExtension, TrigramExtension


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('core', '0069_auto_20210526_1142'),
    ]

    operations = [
        TrigramExtension(),
    ]
