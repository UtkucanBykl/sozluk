from django.contrib.auth import get_user_model
from django.db import models

from ..models import BaseModel

User = get_user_model()

__all__ = ['Follow']


class Follow(BaseModel):
    user = models.ForeignKey(User, related_name='follow', on_delete=models.CASCADE)
    title = models.ForeignKey('core.Title', related_name='follow', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} follow {self.title.title}'
