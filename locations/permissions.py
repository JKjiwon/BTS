from rest_framework import permissions
from .models import Location


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    장소에 대한 권한
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.creator == request.user


class IsCreatordOrReadOnly(permissions.BasePermission):
    """
    사진 성생에 대한 권한, 장소를 만든 사람만 접근 가능
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            location = Location.objects.get(name=request.data["location"])
            return location.creator == request.user


class IsLocationCreatorOrReadOnly(permissions.BasePermission):
    """
    사진 수정에 대한 권한, 장소를 만든 사람만 접근 가능
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.location.creator == request.user
