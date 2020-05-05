from django.utils import timezone
from django.db import models


__all__ = ['BaseModel', 'BaseManager', 'BaseModelQuery', 'BaseModelWithDelete']


class BaseModelQuery(models.QuerySet):
    def delete(self, hard=False):
        if hard:
            return super().delete()
        return super().update(is_deleted=True, deleted_at=timezone.now())

    def actives(self):
        return self.filter(status='publish')


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuery(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()


class BaseModelWithDelete(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(models.Model):

    stages = (
        ('draft', 'draft'),
        ('publish', 'publish')
    )

    status = models.CharField(choices=stages, default='publish', max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, hard=False, *args, **kwargs):
        if hard:
            return super().delete()

        models.signals.pre_delete.send(
            sender=self.__class__,
            instance=self
        )

        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save()
        models.signals.post_delete.send(
            sender=self.__class__,
            instance=self
        )
