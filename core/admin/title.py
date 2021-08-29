from django.contrib import admin
from .base import BaseAdmin

from ..models import Title, Entry, Category, Suggested, NotShowTitle, UserFollow
from .actions import clone_title

__all__ = ['TitleAdmin', 'EntryAdmin', 'CategoryAdmin', 'SuggestedAdmin', 'NotShowTitleAdmin']


@admin.register(Title)
class TitleAdmin(BaseAdmin):
    actions = [clone_title]


@admin.register(Entry)
class EntryAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass


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
    pass
