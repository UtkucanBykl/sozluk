import os
import shutil
import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command


User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if settings.DEBUG is False:
            self.stderr.write(
                self.style.ERROR("You must enable DEBUG mode to run this command.")
            )
            return

        fixtures = [
            "user"
        ]
        for fixture in fixtures:
            self.stdout.write(f"Inserting fixture '{fixture}'...")
            print(f"{settings.FIXTURE_YAML_DIR}/{fixture}")
            if fixture == "user":
                self.load_users()
            else:
                call_command(
                    "loaddata", f"{settings.FIXTURE_YAML_DIR}/{fixture}", format="yaml"
                )

    def load_users(self):
        User.objects.all().delete()
        with open(f"{settings.FIXTURE_DIR}/csv/user.csv") as f:
            reader = csv.reader(f, delimiter=',')
            for count, row in enumerate(reader):
                if count == 0:
                    continue
                print(row[10])
                try:
                    user = User.objects.create(
                        old_id=int(row[0]),
                        first_name=row[1],
                        username=row[2],
                        email=row[3],
                        birth_day=row[10] if row[10] != "NULL" else None,
                        is_show_city=bool(row[8])
                    )
                    print(user)
                except:
                    print(row)
