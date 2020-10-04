from django.contrib import admin
from .base import BaseAdmin

from ..models import Title, Entry, Category, Suggested

__all__ = ['TitleAdmin', 'EntryAdmin', 'CategoryAdmin', 'SuggestedAdmin']


@admin.register(Title)
class TitleAdmin(BaseAdmin):
    pass


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
    list_filter = ("suggested_type", "user")
