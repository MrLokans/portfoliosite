from rest_framework import permissions


class TelegramAuthAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        return hasattr(request, "telegram_user")
