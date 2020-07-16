from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permissions to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attributes.
    """

    def has_object_permissions(self, request, view, obj):
        """
        Read permissions are allowed to any request,
        so we'll always allot GET, HEAD or OPTIONS requests.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`
        return obj.user == request.user
        