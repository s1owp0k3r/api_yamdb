from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """"Permission for the administrator."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """"Permission for the administrator, moderator, author"""
    def has_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        return False
