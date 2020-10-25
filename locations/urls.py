from django.urls import path, include
from locations import views
from rest_framework.routers import DefaultRouter

# 장소에 대한 접근 EndPoint(URL) 생성
urlpatterns = [
    path("", views.LocationList.as_view(), name=views.LocationList.name),
    path("<int:pk>/", views.LocationDetail.as_view(), name=views.LocationDetail.name),
    path("photos/", views.PhotoList.as_view(), name=views.PhotoList.name),
    path("photos/<int:pk>/", views.PhotoDetail.as_view(), name=views.PhotoDetail.name),
]
