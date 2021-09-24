from unittest import skip

from django.contrib.auth import get_user_model

# Create your tests here.
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Report, Entry, Title


User = get_user_model()


__all__ = ['StatisticsTest']


class StatisticsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='utku', password=make_password('1234'), email='ddd@ddd.com', account_type='mod'
        )
        self.user1 = User.objects.create(
            username='utku1', password=make_password('1234'), email='dddd@ddd.com', status="deleted"
        )
        self.user2 = User.objects.create(
            username='utku2', password=make_password('1234'), email='ddddd@ddd.com', is_superuser=True
        )
        self.title = Title.objects.create(
            title='Test'
        )
        self.entry = Entry.objects.create(
            title=self.title, user=self.user, content='aaaaaa'
        )
        self.entry2 = Entry.objects.create(
            title=self.title, user=self.user, content='asdasdaaaaaa'
        )
        self.token = Token.objects.get(user=self.user).key

    def test_get_statistics(self):
        url = reverse_lazy('core:statistics')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)









