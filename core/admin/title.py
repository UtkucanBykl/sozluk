from django.contrib import admin

from ..models import  Title, Entry

__all__ = ['TitleAdmin', 'EntryAdmin']



@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    pass


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass
