import random
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from locations.models import Location
from locations.serializers import LocationSerializer
from .serializers import (
    UserSerializer,
    UserSerializerWithToken,
    ChangePasswordSerializer,
    FindPasswordSerializer,
    FindUsernameSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAdminUserRead
from locations.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class UserList(APIView):
    permission_classes = (IsAdminUserRead,)

    def get(self, request):
        users = User.objects.all()
        if len(users) > 0:
            paginator = StandardResultsSetPagination()
            result_page = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response({}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = LocationSerializer(
            user.favs.all(), many=True, context={"request": request}
        ).data
        return Response(serializer)

    def put(self, request):
        pk = request.data.get("id", None)
        user = request.user

        if pk is not None:
            try:
                room = Location.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes((IsAdminUser,))
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def findPassword(request):
    serializer = FindPasswordSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get("username")
        obj = User.objects.get(username=username)
        new_password = username + str(random.randint(100, 999))
        obj.set_password(new_password)
        obj.save()
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "new_password": new_password,
        }
        return Response(response)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def findUsername(request):
    serializer = FindUsernameSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.data.get("phone_number")
        obj = User.objects.get(phone_number=phone_number)
        username = obj.username
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "username": username,
        }
        return Response(response)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
