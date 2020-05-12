from django.contrib.auth import get_user_model

# Create your tests here.
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ..models import Report


User = get_user_model()


__all__ = ['ReportTest']


class ReportTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='utku', password=make_password('1234'), email='ddd@ddd.com'
        )
        self.user1 = User.objects.create(
            username='utku1', password=make_password('1234'), email='dddd@ddd.com'
        )
        self.token = Token.objects.get(user=self.user).key

    def test_create_report(self):
        url = reverse_lazy('core:report-list-create')
        data = {
            'to_user': self.user1.id,
            'content': 'bad words',
            'report_type': 'toxic',
            'entry': ''
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.data['to_user_detail']['username'], 'utku1')

    def test_get_reports(self):
        data = {
            'from_user': self.user,
            'to_user': self.user1,
            'content': 'bad words',
            'report_type': 'toxic',
        }
        url = reverse_lazy('core:report-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        Report.objects.create(
        **data
        )
        response = self.client.get(url)
        self.assertEqual(
            response.data['results'][0]['to_user_detail']['username'], 'utku1'
        )
