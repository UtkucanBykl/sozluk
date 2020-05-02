from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import override_settings

from django_dramatiq.test import DramatiqTestCase

from ..models import Entry, Title
from ..tasks import update_user_points

User = get_user_model()

all = ['TaskTestCase']


class TaskTestCase(DramatiqTestCase):
    def setUp(self):
        self.title1 = Title.objects.create(
            title='Test'
        )
        self.user = User.objects.create(
            username='Utku', email='utku@can.com', password=make_password('1234')
        )
        self.entry = Entry.objects.create(
            title=self.title1, user=self.user, content='aaaaaa'
        )

    def update_user(self, entry_id, point):
        return update_user_points.send(entry_id, point)

    @override_settings(TEST=True)
    def test_add_like_point(self):
        queue = self.update_user(self.entry.id, 5)
        self.broker.join(queue.queue_name)
        self.worker.join()
        self.assertEqual(User.objects.first().point, 5)
        