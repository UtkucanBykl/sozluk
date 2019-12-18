from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from ..models import Title
from ..serializers import TitleSerializer

__all__ = ['TitleTestCase']

User = get_user_model()


class TitleTestCase(APITestCase):
    def setUp(self):
        self.title1 = Title.objects.create(
            title='Test'
        )
        self.user = User.objects.create(
            username='Utku', email='utku@can.com', password=make_password('1234')
        )
        self.token = Token.objects.get(user=self.user).key

    def test_get_all_active_title(self):
        url = reverse_lazy('core:title-list-create')
        response = self.client.get(url)
        serializer = TitleSerializer(Title.objects.actives(), many=True)
        self.assertEqual(response.data, serializer.data)

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
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
