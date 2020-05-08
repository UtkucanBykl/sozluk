from django.contrib import admin
from .base import BaseAdmin

from ..models import Title, Entry, Category

__all__ = ['TitleAdmin', 'EntryAdmin', 'CategoryAdmin']



@admin.register(Title)
class TitleAdmin(BaseAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    pass