from django.urls import path
from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
    refresh_jwt_token,
)
from . import views
from config.views import validate_jwt_token, CustomObtainJSONWebToken


app_name = "users"
# 회원, 로그인 관련 EndPoint(URL) 생성
urlpatterns = [
    path("", views.UserList.as_view()),
    path("validate/", validate_jwt_token),
    path("login/", obtain_jwt_token),
    path("verify/", verify_jwt_token),
    path("refresh/", refresh_jwt_token),
    path("me/", views.MeView.as_view()),
    path("me/favs/", views.FavsView.as_view()),
    path("<int:pk>/", views.user_detail),
    path("findusername/", views.findUsername),
    path("findpassword/", views.findPassword),
    path("me/changepassword/", views.ChangePasswordView.as_view()),
]
