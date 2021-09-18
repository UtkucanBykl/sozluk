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
        self.user = User.objects.create(
            username='Utku', email='utku@can.com', password=make_password('1234'), is_superuser=True
        )
        self.user2 = User.objects.create(
            username='Utku2', email='ut2ku@can.com', password=make_password('12234')
        )
        self.user3 = User.objects.create(
            username='Utku3', email='ut3ku@can.com', password=make_password('12234'), account_type='mod'
        )
        self.token = Token.objects.get(user=self.user).key
        self.token2 = Token.objects.get(user=self.user2).key
        self.token3 = Token.objects.get(user=self.user3).key

        self.category = Category.objects.create(name='Category')
        self.title1 = Title.objects.create(
            title='Testtttt',
            category=self.category,
            user=self.user2
        )
        self.title2 = Title.objects.create(
            title="Denememee",
            category=self.category
        )

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

    def test_title_create_with_entry(self):
        url = reverse_lazy('core:title-create-with-entry')
        data = {
            'title': [{'title': 'testtetetete'}],
            'entry': [{'content': 'aaaaaqweqweqwe'}]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

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
        NotShowTitle.objects.create(title=self.title2, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        url = reverse_lazy('core:title-list-create')
        response = self.client.get(url)
        self.assertEqual(response.data.get('results'), [])

    def test_fake_delete(self):
        url = reverse_lazy('core:title-update-delete', kwargs={"id": self.title1.id})
        data = {
            "title": "Denememememememe",
            "is_bold": True
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)

    def test_destroy_title_with_superuser(self):
        url = reverse_lazy('core:title-update-delete', kwargs={"id": self.title1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_destroy_title_with_normaluser(self):
        url = reverse_lazy('core:title-update-delete', kwargs={"id": self.title1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_title_combine(self):
        url = reverse_lazy('core:combine-titles')
        data = {
            "from_title": self.title1.pk,
            "to_title": self.title2.pk
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data)
        self.assertEqual(response.data['system_message'], 'Başlıkları birleştirme işlemi başlatıldı.')

    def test_change_tematik_entries_in_title(self):
        url = reverse_lazy('core:change-all-tematik-entries-in-title', kwargs={"id": self.title1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url)
        self.assertEqual(response.data['system_message'], 'Tematik tanımları normale çevirme işlemi başlatıldı.')

    def test_change_tematik_entries_in_title_with_normal_user(self):
        url = reverse_lazy('core:change-all-tematik-entries-in-title', kwargs={"id": self.title1.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)
        response = self.client.post(url)
        self.assertEqual(response.data['error_message'], 'Bu işlemi yapmak için yetkiniz yok.')