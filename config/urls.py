from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from locations.views import ApiRoot
from rest_framework_jwt.views import (
    obtain_jwt_token,
    verify_jwt_token,
    refresh_jwt_token,
)
from .views import validate_jwt_token


urlpatterns = [
    path("", ApiRoot.as_view(), name=ApiRoot.name),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("locations/", include("locations.urls")),
    path("validate/", validate_jwt_token),
    path("login/", obtain_jwt_token),
    path("verify/", verify_jwt_token),
    path("refresh/", refresh_jwt_token),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
