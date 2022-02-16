from django.contrib import admin
from django.contrib.auth import get_user_model

from .base import BaseAdmin

from .actions import clone, clone_user
from ..models import TitleFollow, Like, Notification, Dislike, Block, UserEmotionActivities, PunishUser, Favorite

__all__ = ['UserAdmin']

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseAdmin):
    actions = [clone_user]
    search_fields = ['username', 'email']
    list_display = ('id', 'username', 'email', 'account_type', 'status', 'created_at')


@admin.register(TitleFollow)
class FollowAdmin(BaseAdmin):
    list_display = ('user', 'title')


@admin.register(Like)
class LikeAdmin(BaseAdmin):
    search_fields = ['user__username']
    list_display = ('user', 'entry')


@admin.register(Dislike)
class DislikeAdmin(BaseAdmin):
    search_fields = ['user__username']
    list_display = ('user', 'entry')


@admin.register(Favorite)
class FavoriteAdmin(BaseAdmin):
    search_fields = ['user__username']
    list_display = ('user', 'entry')


@admin.register(Notification)
class NotoficationAdmin(BaseAdmin):
    search_fields = ['sender_user__username', 'receiver_user__username', 'entry__content', 'message']
    list_display = ('sender_user', 'title', 'receiver_user', 'entry', 'is_open', 'message')
    actions = [clone]


@admin.register(Block)
class BlockAdmin(BaseAdmin):
    search_fields = ['user__username', 'blocked_user__username']
    list_display = ('user', 'blocked_user', 'is_message', 'is_entry')


@admin.register(UserEmotionActivities)
class UserEmotionActivitiesAdmin(BaseAdmin):
    search_fields = ['user__username', 'entry__content']
    list_display = ('id', 'user', 'entry', 'activity_type')


@admin.register(PunishUser)
class PunishUserAdmin(BaseAdmin):
    search_fields = ['punished_user__username']
    list_display = ('id', 'punished_user', 'punish_description', 'punish_finish_date', 'status', 'created_at')
