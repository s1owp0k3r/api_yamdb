from rest_framework import permissions

from .models import Role


class IsAdmin(permissions.BasePermission):
    """"Permission for the administrator."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == Role.ADMIN
                or request.user.is_superuser
            )
        return False
