from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.UserList.as_view()),
    path("me/", views.MeView.as_view()),
    path("me/changepassword/", views.ChangePasswordView.as_view()),
    path("me/favs/", views.FavsView.as_view()),
    path("<int:pk>/", views.user_detail),
    path("findusername/", views.findUsername),
    path("findpassword/", views.findPassword),
]