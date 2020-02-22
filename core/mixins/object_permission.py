__all__ = ['OwnerOrReadOnlyMixin']


class OwnerOrReadOnlyMixin:
    field = 'user'
    error_message = 'You are not owner on this obj'

    def check_object_permissions(self, request, obj):
        field = self.field
        if request.method.lower() in ('get', 'options'):
            return super(self).check_object_permissions(request, obj)
        owner = getattr(obj, field, None)
        if not request.user.is_authenticated:
            return self.permission_denied(
                    request, message="You are not login"
                )
        if owner != request.user:
            return self.permission_denied(
                    request, message=self.error_message
                )
        return super(self).check_object_permissions(request, obj)
