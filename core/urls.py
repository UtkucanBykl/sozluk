from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('titles/', TitleListCreateAPIView.as_view(), name='title-list-create'),
    path('titles/<int:id>/', TitleUpdateDestroyAPIView.as_view({"patch": "partial_update", "delete": "destroy"}), name='title-update-delete'),
    path('entries/', EntryListCreateAPIView.as_view(), name='entry-list-create'),
    path('entries/<int:id>/', EntryRetrieveUpdateDestroyAPIView.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name='entry-retrieve-update-delete'),
    path('likes/', LikeListCreateAPIView.as_view(), name='like-list-create'),
    path('titles/follows/', TitleFollowListCreateAPIView.as_view(), name='title-follow-list-create'),
    path('titles/follows/<int:title_id>/', TitleFollowDeleteAPIView.as_view(), name='title-follow-delete'),
    path('reports/', ReportListCreateAPIView.as_view(), name='report-list-create'),
    path('notifications/', NotificationListAPIView.as_view({"get": "list"}), name='notification-list'),
    path('notifications/<int:id>/', NotificationListAPIView.as_view({"patch": "partial_update"}), name='notification-update'),
    path('users/follows/', UserFollowListCreateAPIView.as_view(), name='user-follow-list-create'),
    path('users/follows/<int:following_user_id>/', UserFollowDeleteAPIView.as_view(), name='user-follow-delete'),
    path('users/following/<int:following_user_id>/', UserFollowRetrieveAPIView.as_view(), name='user-follow-get'),
    path('dislikes/', DislikeListCreateAPIView.as_view(), name='dislike-list-create'),
    path('dislikes/<int:entry_id>/', DeleteDislikeAPIView.as_view(), name='dislike-delete'),
    path('likes/<int:entry_id>/', DeleteLikeAPIView.as_view(), name='like-delete'),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path("users/<int:id>/", UserRetrieveUpdateViewSet.as_view({"get": "retrieve"}), name="user-detail"),
    path("users/me/", UserRetrieveUpdateViewSet.as_view({"patch": "partial_update"}), name="user-update"),
    path("suggesteds/", SuggestedViewSet.as_view({"get": "list", "post": "create"}), name="suggested-list-create"),
    path("suggesteds/<int:id>/", SuggestedViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name="suggested-retrieve-update-delete"),
    path("titles/blocks/", NotShowTitleCreateAPIView.as_view({"post": "create"}), name="block-create"),
    path("titles/blocks/<int:title_id>/", NotShowTitleCreateAPIView.as_view({"delete": "destroy"}), name="block-delete"),
    path("users/password/change/", ChangeUserPasswordView.as_view(), name="change-password"),
    path("blocks/",
         BlockUserViewSet.as_view({"post": "create", "get": "list"}),
         name="user-block-create"),
    path("blocks/<int:blocked_user_id>/",
         BlockUserViewSet.as_view({"patch": "partial_update", "delete": "destroy"}),
         name="user-block-retrieve-update-delete"),
    path('favorites/', FavoriteListCreateAPIView.as_view(), name='favorite-list-create'),
    path('favorites/<int:entry_id>/', DeleteFavoriteAPIView.as_view(), name='favorite-delete'),
    path('titlewithentry/', TitleWithEntryCreateAPIView.as_view(), name='title-create-with-entry'),
    path('messages/', MessageListAPIView.as_view(), name='message-list-create'),
    path('similartitles/', SimilarTitleListAPIView.as_view(), name="similar-titles"),
    path('notifications/deleteall/', NotificationDeleteAllAPIView.as_view({"post": "create"}), name="delete-all-notification"),
    path('notifications/seenall/', NotificationSeenAllAPIView.as_view({"post": "create"}), name="seen-all-notification"),
    path('users/search/', UserSearchAPIView.as_view({"get": "list"}), name="user-search"),
    path('user/lastactivities/', UserEmotionActivitiesAPIView.as_view({"get": "list"}), name="user-last-activities"),
    path('titles/combine/', CombineTwoTitles.as_view({"post": "create"}), name="combine-titles"),
    path('titles/<int:id>/changeTematik', ChangeAllTematikEntriesInTitle.as_view({"post": "create"}), name="change-all-tematik-entries-in-title"),
]
