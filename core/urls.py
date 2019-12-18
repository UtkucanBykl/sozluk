from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('titles/', TitleListCreateAPIView.as_view(), name='title-list-create'),
    path('entries/', EntryListCreateAPIView.as_view(), name='entry-list-create'),
    path('entries/<int:id>', EntryRetrieveUpdateDestroyAPIView.as_view(), name='entry-retrieve-update-delete')
]
