from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from ..models import Message

__all__ = ['MessageTestCase']

User = get_user_model()


class MessageTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='pal', email='utku@can.com', password=make_password('1234')
        )
        self.user2 = User.objects.create(
            username='thegallows', email='ut2ku@can.com', password=make_password('12234')
        )

        self.message = Message.objects.create(
            sender_user=self.user,
            receiver_user=self.user2,
            content="How you doin 1"
        )

        self.message = Message.objects.create(
            sender_user=self.user2,
            receiver_user=self.user,
            content="How you doin 2"
        )

        self.message = Message.objects.create(
            sender_user=self.user,
            receiver_user=self.user2,
            content="How you doin 3"
        )

        self.token = Token.objects.get(user=self.user).key

    def test_get_messages(self):
        base_url = reverse_lazy('core:message-list-create')
        url = f'{base_url}?receiver_user=' + str(self.user2.pk)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_message(self):
        url = reverse_lazy('core:message-list-create')
        data = {
            "content": 'Merhabalarrrr',
            "receiver_user": self.user2.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)