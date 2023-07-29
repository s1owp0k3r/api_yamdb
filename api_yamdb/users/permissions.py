from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """"Permission for the administrator."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)