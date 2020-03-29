import os

from django.contrib.auth import get_user_model
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


User = get_user_model()


class Command(createsuperuser.Command):
    help = 'Crate a superuser, and allow password to be provided'

    def handle(self, *args, **options):
        password = os.environ.get('BASIC_USER_PASS', '123')
        try:
            user = User.objects.create_superuser(
                username='test', email='test@test.com', first_name='utku', last_name='can'
                )
            user.set_password(password)
            user.save()
            print('Superuser created')
        except:
            pass