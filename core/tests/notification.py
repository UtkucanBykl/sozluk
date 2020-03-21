from django.contrib.auth import get_user_model

# Create your tests here.
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Notification


User = get_user_model()


__all__ = ['NotificationTest']


class NotificationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='utku', password=make_password('1234'), email='ddd@ddd.com'
        )
        self.user1 = User.objects.create(
            username='utku1', password=make_password('1234'), email='dddd@ddd.com'
        )
        self.token = Token.objects.get(user=self.user).key
        self.notification = Notification.objects.create(
            to_user=self.user, from_user=self.user1, message='Hello', notification_type='info'
        )

    def test_get_notification(self):
        url = reverse_lazy('core:notification-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(
            response.data['results'][0]['from_user_detail']['username'], 'utku1'
        )
