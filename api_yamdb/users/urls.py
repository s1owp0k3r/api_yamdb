from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet, SignUpViewSet, TokenViewSet

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("api/v1/", include(router_v1.urls)),
    path("api/v1/auth/token/", TokenViewSet.as_view()),
    path("api/v1/auth/signup/", SignUpViewSet.as_view()),
]
