from unittest import skip

from django.contrib.auth import get_user_model

# Create your tests here.
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import PunishUser


User = get_user_model()


__all__ = ['PunishTest']


class PunishTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='utku', password=make_password('1234'), email='ddd@ddd.com', is_superuser=True
        )
        self.user1 = User.objects.create(
            username='utku1', password=make_password('1234'), email='dddd@ddd.com'
        )
        self.user2 = User.objects.create(
            username='utku2', password=make_password('1234'), email='ddddd@ddd.com', account_type='mod'
        )
        self.token = Token.objects.get(user=self.user).key
        self.token2 = Token.objects.get(user=self.user1).key
        self.token3 = Token.objects.get(user=self.user2).key

        self.user3 = User.objects.create(
            username='utku3', password=make_password('1234'), email='dddddd@ddd.com'
        )
        self.token4 = Token.objects.get(user=self.user3).key

        self.punish = PunishUser.objects.create(
            punished_user=self.user3, punish_description='Sen ne güzel tweetler atıyorsun öyle.',
            punish_finish_date='2021-12-23', status='deleted'
        )

        self.punish2 = PunishUser.objects.create(
            punished_user=self.user3, punish_description='Sen ne güzel tweetler atıyorsun öyle.',
            punish_finish_date='2022-02-28'
        )

    def test_create_punish_with_superuser_or_mod(self):
        url = reverse_lazy('core:user-penalties')
        data = {
            'punished_user': self.user.pk,
            'punish_description': 'Bak bunu burdan alın',
            'punish_finish_date': '2021-12-23'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.data['punish_finish_date'], '2021-12-23')

        data2 = {
            'punished_user': self.user1.pk,
            'punish_description': 'Bak bunu burdan alın2',
            'punish_finish_date': '2021-12-23'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3)
        response2 = self.client.post(url, data2)
        self.assertEqual(response2.data['punish_finish_date'], '2021-12-23')

    def test_create_punish_with_normal_user(self):
        url = reverse_lazy('core:user-penalties')
        data = {
            'punished_user': self.user.pk,
            'punish_description': 'Bak bunu burdan alın',
            'punish_finish_date': '2021-12-23'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)
        response = self.client.post(url, data)
        self.assertEqual(response.data['error_message'], 'Bu işlemi yapmak için yetkiniz yok.')

    def test_get_user_punish(self):
        url = reverse_lazy('core:user-penalties')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token4)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_with_punished_user(self):
        url = reverse_lazy('core:user-login')
        data = {
            'username': 'utku3',
            'password': '1234'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['status_code'], 401)
