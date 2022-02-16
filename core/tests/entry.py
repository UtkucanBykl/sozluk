from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Entry, Title, Like, Notification, Block, Dislike, Favorite
from ..serializers import LikeSerializer, DislikeSerializer, FavoriteSerializer

__all__ = ['EntryTestCase']

User = get_user_model()


class EntryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='Utku', email='utku@can.com', password=make_password('1234')
        )
        self.superuser = User.objects.create(
            username='tugay', email='tugay@can.com', password=make_password('1234'), is_superuser=True
        )

        self.title1 = Title.objects.create(
            title='Test',
            user=self.superuser
        )
        self.title_cant_write = Title.objects.create(
            title='Testttt',
            can_write=False
        )
        self.token = Token.objects.get(user=self.user).key
        self.token_superuser = Token.objects.get(user=self.superuser).key
        self.entry = Entry.objects.create(
            title=self.title1, user=self.user, content='aaaaaa'
        )
        self.entry2 = Entry.objects.create(
            title=self.title1, user=self.user, content='aaddaaaa', is_tematik=True
        )

        self.Like = Like.objects.create(
            user=self.user, entry=self.entry2
        ) 

    def test_create_entry_without_auth(self):
        url = reverse_lazy('core:entry-list-create')
        data = {
            'title': self.title1,
            'content': 'aaaaa'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    def test_create_entry_with_auth(self):
        url = reverse_lazy('core:entry-list-create')
        data = {
            'content': 'aaaaa',
            'title': self.title1.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_entry_with_error(self):
        url = reverse_lazy('core:entry-list-create')
        data = {
            'content': 'aaaaa',
            'title': self.title_cant_write
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertIsNotNone(response.data.get('fallback_message'))

    def test_update_entry_with_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry.id})
        data = {
            'content': 'bbbbb'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, data)
        self.assertEqual(response.data['content'], 'bbbbb')

    def test_update_entry_with_no_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry.id})
        data = {
            'content': 'bbbbb'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 401)

    def test_delete_entry_with_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_delete_entry_no_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_delete_entry_by_admin(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_superuser)
        response = self.client.delete(url)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.status, 'deleted_by_admin')

    def test_like(self):
        url = reverse_lazy('core:like-list-create')
        data = {
            "entry": self.entry.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_likes_of_entries(self):
        url = reverse_lazy('core:like-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f'{url}?entry_id={self.entry2.id}')
        self.assertEqual(response.status_code, 200)

    def test_dislike(self):
        url = reverse_lazy('core:dislike-list-create')
        data = {
            "entry": self.entry.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(201, response.status_code)

    def test_like_list(self):
        Like.objects.create(user=self.user, entry=self.entry)
        url = reverse_lazy('core:like-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        serializer = LikeSerializer(Like.objects.filter(user=self.user), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_like_list_without_auth(self):
        Like.objects.create(user=self.user, entry=self.entry)
        Like.objects.create(user=self.superuser, entry=self.entry)
        url = reverse_lazy('core:like-list-create') + "?user_id=" + str(self.user.id)
        response = self.client.get(url)
        serializer = LikeSerializer(Like.objects.filter(user=self.user), many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(1, 1)

    def test_dislike_list_without_auth(self):
        Dislike.objects.create(user=self.user, entry=self.entry)
        Dislike.objects.create(user=self.superuser, entry=self.entry)
        url = reverse_lazy('core:dislike-list-create') + "?user_id=" + str(self.user.id)
        response = self.client.get(url)
        serializer = DislikeSerializer(Dislike.objects.filter(user=self.user), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_favorite_list_without_auth(self):
        Favorite.objects.create(user=self.user, entry=self.entry)
        Favorite.objects.create(user=self.superuser, entry=self.entry)
        url = reverse_lazy('core:favorite-list-create') + "?user_id=" + str(self.user.id)
        response = self.client.get(url)
        serializer = FavoriteSerializer(Favorite.objects.filter(user=self.user), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_delete_like(self):
        Like.objects.create(user=self.user, entry=self.entry)
        url = reverse_lazy('core:like-delete', kwargs={'entry_id': self.entry.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertFalse(Like.objects.filter(user=self.user, entry=self.entry).exists())
        self.assertEqual(response.status_code, 204)

    def test_get_entry(self):
        Like.objects.create(user=self.user, entry=self.entry)
        url = reverse_lazy('core:entry-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f'{url}?title={self.title1.id}')
        self.assertEqual(response.status_code, 200)

    def test_get_entry_without_auth(self):
        url = reverse_lazy('core:entry-list-create')
        response = self.client.get(f'{url}?title={self.title1.id}')
        self.assertEqual(response.data.get('results', [])[0]['is_like'], False)

    def test_get_entry_with_auth_control_like(self):
        Like.objects.create(user=self.user, entry=self.entry)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id':self.entry.id})
        response = self.client.get(url)
        self.assertEqual(response.data.get('is_like'), True)

    def test_get_entry_on_block_user(self):
        Block.objects.create(blocked_user=self.user, user=self.superuser)
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_entry_is_tematik(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry2.id})
        response = self.client.get(url)
        self.assertEqual(response.data.get('is_tematik'), True)

    def test_patch_entry_is_tematik(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id': self.entry2.id})
        data = {
            'is_tematik': False
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, data)
        self.assertEqual(response.data.get('is_tematik'), False)
