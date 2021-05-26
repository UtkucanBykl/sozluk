from django.db import models
from django.utils import timezone

from ..models import BaseModel, User

__all__ = ['Message']


class Message(BaseModel):
    sender_user = models.ForeignKey(User, related_name='sender_user', null=False, on_delete=models.CASCADE)
    receiver_user = models.ForeignKey(User, related_name='receiver_user', null=False, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)

    def __str__(self):
        return self.content
