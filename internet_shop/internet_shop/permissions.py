"""
internet_shop project DRF permissions
"""

from rest_framework import permissions

from user.models import UserModel


class IsSuperuserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class UserProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj: UserModel):
        if request.user.is_superuser:
            return True
        return obj == request.user



