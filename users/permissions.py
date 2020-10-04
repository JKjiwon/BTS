from rest_framework import permissions


class IsAdminUserRead(permissions.BasePermission):
    """어드민 유저일 경우 Read 가능"""

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        elif request.method == "GET":
            return bool(request.user and request.user.is_staff)
