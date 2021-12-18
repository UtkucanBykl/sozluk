from django.contrib.auth import get_user_model
from django.test import override_settings
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from PIL import Image

from ..models import Title, Entry, UserFollow, PunishUser

import io
import datetime

User = get_user_model()

__all__ = ['UserTest']


class UserTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='utku', password=make_password('1234'), email='ddd@ddd.com', bio="TEST", is_superuser=True
        )
        self.user1 = User.objects.create(
            username='utku1', password=make_password('1234'), email='d1dd@ddd.com', bio="TEST", show_bio=False
        )
        self.user2 = User.objects.create(
            username='utku2', password=make_password('1234'), email='dddd@ddd.com', bio="TEST", account_type="normal",
        )

        self.user3 = User.objects.create(
            username='utku3', password=make_password('1234'), email='ddddd@ddd.com', bio="TEST", account_type="normal"
        )

        self.follow = UserFollow.objects.create(
            follower_user=self.user2, following_user=self.user1
        )

        self.title = Title.objects.create(
            title="Deneme", user=self.user1
        )

        self.entry = Entry.objects.create(
            title=self.title,
            content="asdasdasd",
            user=self.user
        )
        self.token = Token.objects.get(user=self.user).key
        self.token2 = Token.objects.get(user=self.user1).key
        self.token3 = Token.objects.get(user=self.user2).key

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

    def test_follow_create_and_get_following_users(self):
        url = reverse_lazy('core:user-follow-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            'following_user': self.user1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['following_user_detail']['username'], 'utku1')
        self.user.refresh_from_db()

        url = reverse_lazy('core:user-follow-list-create') + '?query=following_users'
        response = self.client.get(url)
        self.assertEqual(response.data['results'][0]['following_user_detail']['username'], 'utku1')

    def test_follow_create_and_get_follower_users(self):
        url = reverse_lazy('core:user-follow-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)
        data = {
            'following_user': self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['following_user_detail']['username'], 'utku')
        self.user.refresh_from_db()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token3)
        data = {
            'following_user': self.user.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.data['following_user_detail']['username'], 'utku')
        self.user.refresh_from_db()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse_lazy('core:user-follow-list-create') + '?query=users_who_follow'
        response = self.client.get(url)
        self.assertEqual(response.data['results'][0]['following_user_detail']['username'], 'utku')
        self.assertEqual(response.data['results'][1]['following_user_detail']['username'], 'utku')

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

    def test_change_password(self):
        url = reverse_lazy("core:change-password")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        patch_data = {
            "old_password": "utkuutku",
            "new_password": "utku"
        }
        response = self.client.patch(url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        photo_file = file
        url = reverse_lazy('core:user-register')
        data = {
            'username': 'tugay',
            'password': 'celmeli',
            'confirm_password': 'celmeli',
            'kvkk': True,
            'email': 'dd@ddd.com',
            'recaptcha': 'dd',
            'profile_picture': photo_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_user_city_gender_birth_day(self):
        url = reverse_lazy("core:user-detail", kwargs={"id": self.user1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.data.get("city"), "")
        self.assertEqual(response.data.get("is_show_city"), False)
        self.assertEqual(response.data.get("birth_day"), None)
        self.assertEqual(response.data.get("is_show_birth_day"), False)
        self.assertEqual(response.data.get("gender"), "uncertain")
        self.assertEqual(response.data.get("is_show_gender"), False)
        self.assertEqual(response.data.get("twitter_username"), "")
        self.assertEqual(response.data.get("facebook_profile"), "")
        self.assertEqual(response.data.get("account_type"), "rookie")

    def test_update_user_all_variable(self):
        url = reverse_lazy("core:user-update")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        data = {
            "city": "İstanbul",
            "is_show_city": True,
            "birth_day": "1996-12-23",
            "is_show_birth_day": True,
            "gender": "male",
            "is_show_gender": True,
            "twitter_username": "@john.doe",
            "facebook_profile": "https://www.facebook.com/example",
        }
        response = self.client.patch(url, data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.city, "İstanbul")
        self.assertEqual(self.user.is_show_city, True)
        self.assertEqual(self.user.birth_day, datetime.date(1996, 12, 23))
        self.assertEqual(self.user.is_show_birth_day, True)
        self.assertEqual(self.user.gender, "male")
        self.assertEqual(self.user.is_show_gender, True)
        self.assertEqual(self.user.twitter_username, "@john.doe")
        self.assertEqual(self.user.facebook_profile, "https://www.facebook.com/example")

    def test_user_permissions(self):
        url = reverse_lazy("core:have-permission", kwargs={'type': 'entry', 'id': self.entry.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.data['access'], True)
