from django.contrib.auth import get_user_model
from django.db import models

from ..models import BaseModel

__all__ = ['PunishUser']

User = get_user_model()


class PunishUser(BaseModel):
    punished_user = models.ForeignKey(User, on_delete=models.CASCADE)
    punish_description = models.TextField(max_length=500)
    punish_finish_date = models.DateField(verbose_name="Punish date", null=True, blank=True)

    def __str__(self):
        return f"{self.punished_user.username if self.punished_user is not None else '-'} - {self.punish_finish_date} tarihine kadar cezalısınız."
