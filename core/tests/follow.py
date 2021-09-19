from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy

from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase

from ..models import User, UserFollow

__all__ = ['FollowTestCase']

User = get_user_model()


class FollowTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='Utku', email='utku@can.com', password=make_password('1234')
        )

        self.user2 = User.objects.create(
            username='tugay', email='tugay@can.com', password=make_password('1234'), is_superuser=True
        )

        self.user3 = User.objects.create(
            username='sayid', email='sayid@can.com', password=make_password('1234'), is_superuser=True
        )

        self.token = Token.objects.get(user=self.user).key
        self.token_superuser = Token.objects.get(user=self.user2).key

        self.user_follow = UserFollow.objects.create(
            follower_user=self.user, following_user=self.user2
        )

    def test_get_followers(self):
        url = reverse_lazy('core:user-follow-get', kwargs={'following_user_id': self.user2.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.data['is_following'], False)

    def test_create_follow(self):
        url = reverse_lazy('core:user-follow-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'following_user': self.user2.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['error_message'], 'Bu kullanıcıyı zaten takip ediyorsunuz.')

    def test_delete_follow(self):
        url = reverse_lazy('core:user-follow-delete', kwargs={'following_user_id': self.user2.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)