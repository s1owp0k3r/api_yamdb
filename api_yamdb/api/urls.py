from rest_framework import routers
from django.urls import path, include
from api.views import *


router_v1 = routers.DefaultRouter()

urlpatterns = [
    path("", include(router_v1.urls))
]
