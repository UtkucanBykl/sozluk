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
            sender_user=self.user1, receiver_user=self.user, message='Hello', notification_type='info'
        )

    def test_get_notification(self):
        url = reverse_lazy('core:notification-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(
            response.data['results'][0]['message'], 'Hello'
        )

    def test_update_is_seen(self):
        base_url = f'/api/notifications/' + str(self.notification.pk) + '/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'is_seen': True,
            'is_deleted': True
        }
        response = self.client.patch(base_url, data)
        self.assertEqual(response.data['is_deleted'], True)
        self.assertEqual(response.data['is_seen'], True)
