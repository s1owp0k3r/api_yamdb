from rest_framework import mixins, response, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail.message import EmailMessage
from django.shortcuts import get_object_or_404

from users.models import User

from .mixins import UpdateModelMixin
from .permissions import IsAdmin
from .serializers import (ProfileSerializer, SignUpSerializer, TokenSerializer,
                          UserSerializer)


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """User viewset."""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
        url_path="me",
    )
    def profile(self, request):
        if request.method == "PATCH":
            serializer = ProfileSerializer(
                self.request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        serializer = ProfileSerializer(self.request.user)
        return response.Response(serializer.data)


class SignUpViewSet(views.APIView):
    """User registration."""

    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        if not User.objects.filter(username=username, email=email).exists():
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        user = User.objects.get_or_create(username=username, email=email)[0]
        confirmation_code = default_token_generator.make_token(user)
        message = EmailMessage(
            body=f"Confirmation code for {user.username}: {confirmation_code}",
            to=(request.data["email"],),
        )
        message.send(fail_silently=True)
        return response.Response(request.data, status=status.HTTP_200_OK)


class TokenViewSet(views.APIView):
    """Getting a token."""

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.validated_data["confirmation_code"]
        if default_token_generator.check_token(user, confirmation_code):
            token = RefreshToken.for_user(user)
            return response.Response({"Token": str(token.access_token)})
        return response.Response(
            {"Error": "Invalid access code."},
            status=status.HTTP_400_BAD_REQUEST,
        )
