from django.contrib import admin
from django.contrib.auth import get_user_model

from .actions import clone, clone_user
from ..models import TitleFollow, Like, Notification, Dislike, Block, UserEmotionActivities

__all__ = ['UserAdmin']

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    actions = [clone_user]
    list_display = ('username', 'email', 'status')


@admin.register(TitleFollow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry')


@admin.register(Dislike)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry')


@admin.register(Notification)
class NotoficationAdmin(admin.ModelAdmin):
    list_display = ('sender_user', 'title', 'receiver_user', 'entry', 'is_open', 'message')
    actions = [clone]


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    pass


@admin.register(UserEmotionActivities)
class UserEmotionActivitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'entry', 'activity_type')
