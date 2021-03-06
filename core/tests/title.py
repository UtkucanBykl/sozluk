from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from ..models import Title, Category, Entry, TitleFollow, UserFollow, NotShowTitle
from ..serializers import TitleSerializer

__all__ = ['TitleTestCase']

User = get_user_model()


class TitleTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Category')
        self.title1 = Title.objects.create(
            title='Testtttt',
            category=self.category
        )
        self.user = User.objects.create(
            username='Utku', email='utku@can.com', password=make_password('1234')
        )
        self.user2 = User.objects.create(
            username='Utku2', email='ut2ku@can.com', password=make_password('12234')
        )
        self.token = Token.objects.get(user=self.user).key

    def test_get_all_active_title(self):
        url = reverse_lazy('core:title-list-create')
        response = self.client.get(url)
        serializer = TitleSerializer(Title.objects.actives(), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_title_with_query(self):
        base_url = reverse_lazy('core:title-list-create')
        url = f'{base_url}?category=Cat'
        response = self.client.get(url)
        serializer = TitleSerializer(Title.objects.filter(category__name__iexact='Cat'), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_title_with_full_text(self):
        base_url = reverse_lazy('core:title-list-create')
        url = f'{base_url}?full_text=Testtttt'
        response = self.client.get(url)
        serializer = TitleSerializer(Title.objects.filter(title__icontains='Te'), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_title_query(self):
        base_url = reverse_lazy('core:title-list-create')
        url = f'{base_url}?title=Utku'
        response = self.client.get(url)
        serializer = TitleSerializer(Title.objects.filter(title__iexact='Utku'), many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_create_title_correct(self):
        url = reverse_lazy('core:title-list-create')
        data = {
            'title': 'Test1'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        serializer = TitleSerializer(Title.objects.filter(title='Test1').first())
        self.assertEqual(response.data, serializer.data)

    def test_create_title_incorrect(self):
        url = reverse_lazy('core:title-list-create')
        data = {
            'title': 'Test'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 401)

    def test_follow(self):
        url = reverse_lazy('core:title-follow-list-create')
        data = {
            'title': self.title1.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_follow_delete(self):
        TitleFollow.objects.create(user=self.user, title=self.title1)
        url = reverse_lazy('core:title-follow-delete', kwargs={"title_id": self.title1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_user_follow_delete(self):
        UserFollow.objects.create(follower_user=self.user, following_user=self.user2)
        url = reverse_lazy('core:user-follow-delete', kwargs={"following_user_id": self.user2.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_have_user_entries_title(self):
        Entry.objects.create(
            title=self.title1,
            user=self.user,
            content='ddd'

        )
        Entry.objects.create(
            title=self.title1,
            user=self.user,
            content='ddd'

        )
        self.assertEquals(2, Title.objects.have_user_entries(self.user).count())

    def test_get_titles_without_not_show(self):
        NotShowTitle.objects.create(title=self.title1, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse_lazy('core:title-list-create')
        response = self.client.get(url)
        self.assertEqual(response.data.get('results'), [])