from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .permissions import IsOwnerOrReadOnly, IsLocationCreatorOrReadOnly
from .permissions import IsCreatordOrReadOnly
from locations.serializers import LocationSerializer
from locations.serializers import PhotoSerializer
from . import models


class PhotoList(generics.ListCreateAPIView):
    """
    사진 (읽기, 생성)에 관한 EndPoint
    """

    queryset = models.Photo.objects.all()
    serializer_class = PhotoSerializer
    name = "photo-list"

    # 회원이면서 장소의 작성자만 사진 생성 가능, 나머지는 읽기만 가능
    permission_classes = (IsAuthenticatedOrReadOnly, IsCreatordOrReadOnly)
    # 인증은 JWT 토큰으로만 가능
    authentication_classes = (JSONWebTokenAuthentication,)


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    사진 (검색,수정,삭제)에 관한 EndPoint
    """

    queryset = models.Photo.objects.all()
    serializer_class = PhotoSerializer
    name = "photo-detail"

    # 회원이면서 장소의 작성자만 수정,삭제 가능, 나머지는 검색만 가능
    permission_classes = (IsAuthenticatedOrReadOnly, IsLocationCreatorOrReadOnly)
    # 인증은 JWT 토큰으로만 가능
    authentication_classes = (JSONWebTokenAuthentication,)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class LocationList(generics.ListCreateAPIView):
    """
    장소 (읽기, 생성)에 관한 EndPoint
    """

    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    name = "location-list"

    # 회원만 장소 생성가능, 나머지는 읽기만 가능
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # 인증은 JWT 토큰으로만 가능
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
    """
    장소 (검색,수정,삭제)에 관한 EndPoint
    """

    queryset = models.Location.objects.all()
    serializer_class = LocationSerializer
    name = "location-detail"

    # 회원이면서 장소 작성자만 장소 수정 가능, 나머지는 검색만 가능
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    # 인증은 JWT 토큰으로만 가능
    authentication_classes = (JSONWebTokenAuthentication,)

    # PUT으로 부분 수정 가능하도록 설정
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ApiRoot(generics.GenericAPIView):
    name = "api-root"
    permission_classes = []
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        return Response({"locations": reverse(LocationList.name, request=request),})
