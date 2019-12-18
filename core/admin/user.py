from django.contrib import admin
from django.contrib.auth import get_user_model

__all__ = ['UserAdmin']

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'status')
