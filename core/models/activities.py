from django.contrib.auth import get_user_model
from django.db import models

from ..models import BaseModel, Entry

User = get_user_model()

__all__ = ['UserEmotionActivities']


class UserEmotionActivities(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey('core.Entry', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.entry.content}'
