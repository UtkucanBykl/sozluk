from rest_framework.permissions import BasePermission

__all__ = ['IsOwnerOrReadOnly']


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be owner of this object."
    safe_methods = ['GET']
    field = 'user'

    def has_object_permission(self, request, view, obj):
        if request.method in self.safe_methods:
            return True
        if request.user.is_superuser:
            return True
        elif obj.user == request.user:
            return True
        else:
            return False
