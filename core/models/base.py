from django.db.models import Q
from django.utils import timezone
from django.db import models


__all__ = ['BaseModel', 'BaseManager', 'BaseModelQuery', 'BaseModelWithDelete']


class BaseModelQuery(models.QuerySet):
    def delete(self, hard=False):
        if hard:
            return super().delete()
        return super().update(status='deleted', deleted_at=timezone.now())

    def actives(self):
        return self.filter(status='publish')

    def deletes_or_actives(self):
        return self.filter(Q(status='publish')|Q(status='deleted'))


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseModelQuery(self.model, using=self._db)

    def actives(self):
        return self.get_queryset().actives()

    def deletes_or_actives(self):
        return self.get_queryset().deletes_or_actives()


class BaseModelWithDelete(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class BaseModel(models.Model):

    stages = (
        ('draft', 'draft'),
        ('publish', 'publish'),
        ('deleted', 'deleted')
    )

    status = models.CharField(choices=stages, default='publish', max_length=25)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncelleme Tarihi")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Silme Tarihi")

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

        self.status = 'deleted'
        self.deleted_at = timezone.now()

        self.save()
        models.signals.post_delete.send(
            sender=self.__class__,
            instance=self
        )
