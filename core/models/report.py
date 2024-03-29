from django.contrib.auth import get_user_model
from django.db import models

from ..models import BaseModel

__all__ = ['Report']

User = get_user_model()


class Report(BaseModel):
    report_type_choices = (
        ('toxic', 'toxic'),
        ('error', 'error'),
        ('insult', 'insult'),
        ('undefined', 'undefined'),
        ('illegal', 'illegal'),
        ('dirtywords', 'dirty words')
    )
    from_user = models.ForeignKey(User, related_name='send_report', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Şikayet Eden")
    entry = models.ForeignKey('core.Entry', related_name='reports', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Girdi")
    to_user = models.ForeignKey(User, related_name='get_report', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Şikayet Edilen")
    report_type = models.CharField(choices=report_type_choices, max_length=48, verbose_name="Rapor Tipi")

    def __str__(self):
        return f"{self.from_user.username if self.from_user is not None else '-'} -> {self.to_user.username if self.to_user is not None else self.entry.content}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_user", "to_user"], name="unique_from_user_to_user"),
            models.UniqueConstraint(fields=["from_user", "entry"], name="unique_from_user_entry")
        ]
