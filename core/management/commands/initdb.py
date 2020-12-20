import os
import shutil
import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command


from ...models import Title, Entry

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if settings.DEBUG is False:
            self.stderr.write(
                self.style.ERROR("You must enable DEBUG mode to run this command.")
            )
            return

        fixtures = [
            #"user",
            #"title",
            "entries",
        ]
        for fixture in fixtures:
            self.stdout.write(f"Inserting fixture '{fixture}'...")
            print(f"{settings.FIXTURE_YAML_DIR}/{fixture}")
            if fixture == "user":
                self.load_users()
            elif fixture == "title":
                self.load_titles()
            elif fixture == "entries":
                self.load_entries()
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
                try:
                    user = User.objects.create(
                        old_id=int(row[0]),
                        first_name=row[1],
                        username=row[2],
                        email=row[3],
                        birth_day=row[10] if row[10] != "NULL" else None,
                        is_show_city=bool(row[8])
                    )
                    print(User.objects.count())
                    print(User.objects.last().old_id)
                except:
                    print(row)

    def load_titles(self):
        with open(f"{settings.FIXTURE_DIR}/csv/title.csv") as f:
            Title.objects.all().delete(hard=True)
            reader = csv.reader(f, delimiter=',')
            for count, row in enumerate(reader):
                try:
                    if count == 0:
                        continue
                    user = None
                    if User.objects.filter(old_id=int(row[4])).exists():
                        user = User.objects.filter(old_id=int(row[4])).first()
                    status = "deleted" if row[10] == "1" else "draft" if row[14] == "1" else "publish"
                    Title.objects.create(
                        old_id=int(row[0]),
                        title=row[2],
                        user=user,
                        created_at=row[5],
                        updated_at=row[5],
                        status=status,
                        can_write=int(bool(row[12])),
                        is_bold=int(bool(row[11])),
                        deleted_at=row[7] if row[7] != "NULL" else None
                    )
                    print(count)
                except BaseException as e:
                    print(e)

    def load_entries(self):
        with open(f"{settings.FIXTURE_DIR}/csv/entries.csv") as f:
            Entry.objects.all().delete(hard=True)
            reader = csv.reader(f, delimiter=',')
            for count, row in enumerate(reader):
                if count == 0:
                    continue
                try:
                    print(row)
                    data = {
                        "old_id": int(row[0]),
                        "title": Title.objects.get(old_id=int(row[1])),
                        "user": User.objects.get(old_id=int(row[2])),
                        "content": row[4],
                        "created_at": row[5],
                        "deleted_at": row[9] if row[9] != "NULL" else None,
                        "status": "deleted" if row[13] == "1" else "publish_by_rookie" if row[22] == "1" else "publish",
                        "is_tematik": int(row[20])
                    }
                    Entry.objects.create(**data)
                except BaseException as e:
                    print(e)
