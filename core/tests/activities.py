from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from ..models import UserEmotionActivities, Entry, Title

__all__ = ['Activities']

User = get_user_model()


class Activities(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='pal', email='utku@can.com', password=make_password('1234')
        )

        self.token = Token.objects.get(user=self.user).key

        self.title = Title.objects.create(
            title='Test', user=self.user
        )

        self.entry = Entry.objects.create(
            title=self.title, user=self.user, content='aaaaaa'
        )

        self.activity1 = UserEmotionActivities.objects.create(
            user=self.user, entry=self.entry
        )

    def test_create_activity(self):
        url = reverse_lazy('core:user-last-activities')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
