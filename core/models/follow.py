from django.contrib.auth import get_user_model
from django.db import models

from ..models import BaseModel

User = get_user_model()

__all__ = ['TitleFollow', 'UserFollow']


class TitleFollow(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    title = models.ForeignKey('core.Title', related_name='follows', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} follow {self.title.title}'


class UserFollow(BaseModel):
    follower_user = models.ForeignKey(User, related_name='followings', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} '
