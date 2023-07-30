from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """"Permission for the administrator."""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin
        return False
