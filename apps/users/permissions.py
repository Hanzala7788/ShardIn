from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission:
    - Allow only admins to create/update/delete
    - Non-admins can only read (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
        if request.method in SAFE_METHODS:
            return True
        else:
            return False
