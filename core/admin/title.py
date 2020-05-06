from django.contrib import admin
from .base import BaseAdmin

from ..models import Title, Entry

__all__ = ['TitleAdmin', 'EntryAdmin']



@admin.register(Title)
class TitleAdmin(BaseAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(BaseAdmin):
    pass
