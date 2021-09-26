from django.contrib.auth import get_user_model
from django.db import models

from ..models import BaseModel

__all__ = ["Suggested"]

User = get_user_model()


class Suggested(BaseModel):
    class SuggestedType(models.TextChoices):
        TITLE = "title", "title"
        general = "general", "general"

    suggested_type = models.CharField(max_length=40, choices=SuggestedType.choices, default=SuggestedType.general)
    user = models.ForeignKey(User, related_name="suggestions", on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    title = models.ForeignKey("core.Title", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Suggested"
        verbose_name_plural = "Suggestions"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.suggested_type} - {self.user.username if self.user is not None else None}"
