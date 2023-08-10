from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .yasg import urlpatterns as swagger_urlpatterns
urlpatterns = [
    path("admin/", admin.site.urls),
]

# Apps
urlpatterns +=[
    path('', include("core.urls"), name='core'),
]

# 3th party apps
urlpatterns += [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api-auth/", include("rest_framework.urls")),
]

urlpatterns += swagger_urlpatterns
