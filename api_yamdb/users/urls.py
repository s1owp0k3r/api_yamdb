from rest_framework import routers
from django.urls import path, include

from .views import UserViewSet

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("api/v1/", include(router_v1.urls))
]
