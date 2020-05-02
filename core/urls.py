from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('titles/', TitleListCreateAPIView.as_view(), name='title-list-create'),
    path('entries/', EntryListCreateAPIView.as_view(), name='entry-list-create'),
    path('entries/<int:id>', EntryRetrieveUpdateDestroyAPIView.as_view(), name='entry-retrieve-update-delete'),
    path('likes/', LikeListCreateAPIView.as_view(), name='like-list-create'),
    path('follows/', FollowListCreateAPIView.as_view(), name='follow-list-create'),
    path('reports/', ReportListCreateAPIView.as_view(), name='report-list-create'),
<<<<<<< Updated upstream
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list')
=======
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('users/follows/', UserFollowListCreateAPIView.as_view(), name='user-follow-list-create'),
    path('dislikes/', DislikeListCreateAPIView.as_view(), name='dislike-list-create'),
>>>>>>> Stashed changes

]
