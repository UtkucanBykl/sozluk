from django.contrib.auth import get_user_model
from django.db import models

from ..models import BaseModel, Entry, Title

__all__ = ['Notification']

User = get_user_model()


class Notification(BaseModel):
    follow = 'follow'
    like = 'like'
    mention = 'mention'
    info = 'info'
    favorite = 'favorite'
    username_title = 'username_title'
    dislike = 'dislike'
    info_title_entries = 'info_title_entries'
    notification_types = (
        (follow, follow),
        (like, like),
        (mention, mention),
        (info, info),
        (favorite, favorite),
        (username_title, username_title),
        (dislike, dislike),
        (info_title_entries, info_title_entries)
    )
    notification_type = models.CharField(max_length=25, choices=notification_types, default='info')
    receiver_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    sender_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, blank=True, null=True, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, blank=True, null=True, on_delete=models.CASCADE)
    message = models.CharField(max_length=140)
    redirect = models.URLField(blank=True, null=True, max_length=500)
    is_open = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.message
