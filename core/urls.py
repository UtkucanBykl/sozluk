from django.urls import path
from .views import *

app_name = 'core'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('titles/', TitleListCreateAPIView.as_view(), name='title-list-create'),
    path('entries/', EntryListCreateAPIView.as_view(), name='entry-list-create'),
    path('entries/<int:id>/', EntryRetrieveUpdateDestroyAPIView.as_view(), name='entry-retrieve-update-delete'),
    path('likes/', LikeListCreateAPIView.as_view(), name='like-list-create'),
    path('titles/follows/', TitleFollowListCreateAPIView.as_view(), name='title-follow-list-create'),
    path('titles/follows/<int:title_id>/', TitleFollowDeleteAPIView.as_view(), name='title-follow-delete'),
    path('reports/', ReportListCreateAPIView.as_view(), name='report-list-create'),
    path('notifications/', NotificationListAPIView.as_view(), name='notification-list'),
    path('users/follows/', UserFollowListCreateAPIView.as_view(), name='user-follow-list-create'),
    path('users/follows/<int:following_user_id>/', UserFollowDeleteAPIView.as_view(), name='user-follow-delete'),
    path('dislikes/', DislikeListCreateAPIView.as_view(), name='dislike-list-create'),
    path('dislikes/<int:entry_id>/', DeleteDislikeAPIView.as_view(), name='dislike-delete'),
    path('likes/<int:entry_id>/', DeleteLikeAPIView.as_view(), name='like-delete'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path("users/<int:id>/", UserRetrieveUpdateViewSet.as_view({"get": "retrieve"}), name="user-detail"),
    path("users/me/", UserRetrieveUpdateViewSet.as_view({"patch": "update"}), name="user-update"),
    path("suggesteds/", SuggestedViewSet.as_view({"get": "list", "post": "create"}), name="suggested-list-create"),
    path("suggesteds/<int:id>/", SuggestedViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name="suggested-retrieve-update-delete"),
    path("titles/blocks/", NotShowTitleCreateAPIView.as_view({"post": "create"}), name="block-create"),
    path("titles/blocks/<int:title_id>/", NotShowTitleCreateAPIView.as_view({"delete": "destroy"}), name="block-delete"),
    path("users/password/change/", ChangeUserPasswordView.as_view(), name="change-password"),

]
