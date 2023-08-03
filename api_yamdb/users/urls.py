from rest_framework import routers

from django.urls import include, path

from .views import SignUpViewSet, TokenViewSet, UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("api/v1/", include(router_v1.urls)),
    path("api/v1/auth/token/", TokenViewSet.as_view()),
    path("api/v1/auth/signup/", SignUpViewSet.as_view()),
]
