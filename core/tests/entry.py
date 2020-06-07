from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Entry, Title, Like, Notification
from ..serializers import LikeSerializer

__all__ = ['EntryTestCase']

User = get_user_model()


class EntryTestCase(APITestCase):
    def setUp(self):
        self.title1 = Title.objects.create(
            title='Test'
        )
        self.title_cant_write = Title.objects.create(
            title='Testttt',
            can_write=False
        )
        self.user = User.objects.create(
            username='Utku', email='utku@can.com', password=make_password('1234')
        )
        self.token = Token.objects.get(user=self.user).key
        self.entry = Entry.objects.create(
            title=self.title1, user=self.user, content='aaaaaa'
        )
        self.entry = Entry.objects.create(
            title=self.title1, user=self.user, content='aaddaaaa'
        )

    def test_create_entry_without_auth(self):
        url = reverse_lazy('core:entry-list-create', kwargs={'title_id': self.title1.id})
        data = {
            'title': self.title1,
            'content': 'aaaaa'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    def test_create_entry_with_auth(self):
        url = reverse_lazy('core:entry-list-create', kwargs={'title_id': self.title1.id})
        data = {
            'content': 'aaaaa'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, 201)

    def test_create_entry_with_error(self):
        url = reverse_lazy('core:entry-list-create', kwargs={'title_id': self.title_cant_write.id})
        data = {
            'content': 'aaaaa'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertIsNotNone(response.data.get('fallback_message'))

    def test_update_entry_with_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id':self.entry.id, 'title_id': self.title1.id})
        data = {
            'content': 'bbbbb'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, data)
        self.assertEqual(response.data['content'], 'bbbbb')

    def test_update_entry_with_no_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id':self.entry.id, 'title_id': self.title1.id})
        data = {
            'content': 'bbbbb'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 401)

    def test_delete_entry_with_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id':self.entry.id, 'title_id': self.title1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_delete_entry_no_auth(self):
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id':self.entry.id, 'title_id': self.title1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_like(self):
        url = reverse_lazy('core:like-list-create')
        data = {
            "entry": self.entry.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

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

    def test_get_entry(self):
        Like.objects.create(user=self.user, entry=self.entry)
        url = reverse_lazy('core:entry-list-create', kwargs={'title_id': self.title1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_entry_without_auth(self):
        url = reverse_lazy('core:entry-list-create', kwargs={'title_id': self.title1.id})
        response = self.client.get(url)
        self.assertEqual(response.data.get('results', [])[0]['is_like'], False)

    def test_get_entry_with_auth_control_like(self):
        Like.objects.create(user=self.user, entry=self.entry)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse_lazy('core:entry-retrieve-update-delete', kwargs={'id':self.entry.id, 'title_id': self.title1.id})
        response = self.client.get(url)
        self.assertEqual(response.data.get('is_like'), True)
