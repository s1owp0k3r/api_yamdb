from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """"Permission for the administrator."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)
