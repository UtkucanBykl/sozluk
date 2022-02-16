from django.contrib import admin
from .base import BaseAdmin

from ..models import Title, Entry, Suggested, NotShowTitle, UserFollow
from .actions import clone_title

__all__ = ['TitleAdmin', 'EntryAdmin', 'SuggestedAdmin', 'NotShowTitleAdmin']


@admin.register(Title)
class TitleAdmin(BaseAdmin):
    actions = [clone_title]
    search_fields = ['title']
    list_display = ('id', 'title', 'is_ukde', 'created_at')


@admin.register(Entry)
class EntryAdmin(BaseAdmin):
    search_fields = ['content']
    list_display = ('id', 'content', 'status', 'created_at')


@admin.register(Suggested)
class SuggestedAdmin(BaseAdmin):
    list_select_related = ("user", "title")
    list_display = ("user", "message", "title", "suggested_type")
    list_filter = ("suggested_type",)


@admin.register(NotShowTitle)
class NotShowTitleAdmin(BaseAdmin):
    pass


@admin.register(UserFollow)
class UserFollowAdmin(BaseAdmin):
    list_display = ('id', 'follower_user', 'following_user', 'status', 'created_at')
