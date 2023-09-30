from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOnlyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.role == User.ADMIN
            )


class IsAuthorOrAdminReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (
                request.user.is_authenticated
                and (
                    request.user.is_staff
                    or request.user.is_superuser
                    or request.user.role == User.ADMIN
                )
            )
        )


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.role == User.ADMIN
            )
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
                or request.user.role == User.ADMIN
            )
        )
