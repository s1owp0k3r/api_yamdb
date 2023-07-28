from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated


from users.models import User
from .serializers import UserSerializer
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """Create user."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
