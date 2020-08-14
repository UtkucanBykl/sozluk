from rest_framework.permissions import BasePermission, DjangoModelPermissions

__all__ = ['IsOwnerOrReadOnly', 'OwnModelPermission']


class OwnModelPermission(DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


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
