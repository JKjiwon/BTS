from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .permissions import IsOwnerOrReadOnly, IsLocationCreatorOrReadOnly
from .permissions import CreatePermission
from locations.serializers import LocationSerializer
from locations.serializers import PhotoSerializer
from . import models


class PhotoList(generics.ListCreateAPIView):
    queryset = models.Photo.objects.all()
    serializer_class = PhotoSerializer
    name = "photo-list"
    permission_classes = (IsAuthenticatedOrReadOnly, CreatePermission)
    authentication_classes = (JSONWebTokenAuthentication,)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Photo.objects.all()
    serializer_class = PhotoSerializer
    name = "photo-detail"

    # 사진 수정, 삭제 => 로그인한 사용자 and 장소 작성자
    permission_classes = (IsAuthenticatedOrReadOnly, IsLocationCreatorOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LocationList(generics.ListCreateAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    name = "location-list"

    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    filter_fields = (
        "name",
        "city",
        "category",
        "creator",
    )
    search_fields = ("name", "city", "description")
    ordering_fields = (
        "name",
        "city",
    )


class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    name = "location-detail"

    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    authentication_classes = (JSONWebTokenAuthentication,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ApiRoot(generics.GenericAPIView):
    name = "api-root"
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response({"locations": reverse(LocationList.name, request=request),})
