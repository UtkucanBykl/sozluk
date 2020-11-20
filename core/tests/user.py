from django.contrib.auth import get_user_model
from django.test import override_settings
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


__all__ = ['UserTest']


class UserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='utku', password=make_password('1234'), email='ddd@ddd.com', bio="TEST"
        )
        self.user1 = User.objects.create(
            username='utku1', password=make_password('1234'), email='d1dd@ddd.com', bio="TEST", show_bio=False
        )
        self.token = Token.objects.get(user=self.user).key

    @override_settings(DRF_RECAPTCHA_TESTING=True)
    def test_register(self):
        url = reverse_lazy('core:user-register')
        data = {
            'username': 'utkucan',
            'password': 'utkuutku',
            'confirm_password': 'utkuutku',
            'kvkk': True,
            'email': 'dd@ddd.com',
            'recaptcha': 'dd'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        url = reverse_lazy('core:user-login')
        data = {
            'username': 'utku',
            'password': '1234'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_register_fail(self):
        url = reverse_lazy('core:user-register')
        data = {
            'username': 'utku',
            'password': 'utkuutku',
            'confirm_password': 'utkuutku',
            'kvkk': True,
            'email': 'ddcom'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_fail(self):
        url = reverse_lazy('core:user-login')
        data = {
            'username': 'utku',
            'password': '12344'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_follow(self):
        url = reverse_lazy('core:user-follow-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'following_user': self.user1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['following_user_detail']['username'], 'utku1')

    def test_get_user(self):
        url = reverse_lazy("core:user-detail", kwargs={"id": self.user1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.data.get("bio"), "")

    def test_update_user_without_correct_url(self):
        url = reverse_lazy("core:user-detail", kwargs={"id": self.user1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        patch_data = {
            "first_name": "test"
        }
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        url = reverse_lazy("core:user-update")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        patch_data = {
            "bio": "test bio"
        }
        response = self.client.patch(url, patch_data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, patch_data.get("bio"))
