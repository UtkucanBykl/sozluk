from django.contrib import admin
from django.contrib.auth import get_user_model

from ..models import Follow, Like, Notification

__all__ = ['UserAdmin']

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'status')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry')


@admin.register(Notification)
class NotoficationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'title', 'from_user', 'entry', 'is_open')
