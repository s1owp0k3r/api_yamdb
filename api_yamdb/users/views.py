from rest_framework import viewsets, views, response, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.core import exceptions
from django.core.mail.message import EmailMessage
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from users.models import User
from .serializers import UserSerializer, TokenSerializer, SignUpSerializer
from .permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """User viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ("username",)


class SignUpViewSet(views.APIView):
    """User registration."""
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            user = User.objects.get(
                username=request.data["username"],
                email=request.data["email"]
            )
        except exceptions.ObjectDoesNotExist:
            serializer = SignUpSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        message = EmailMessage(
            body=f"Сonfirmation code for {user.username}: {confirmation_code}",
            to=(request.data["email"],),
        )
        message.send(fail_silently=True)
        return response.Response(request.data, status=status.HTTP_200_OK)


class TokenViewSet(views.APIView):
    """Getting a token."""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.validated_data["confirmation_code"]
            if default_token_generator.check_token(user, confirmation_code):
                token = RefreshToken.for_user(user)
                return response.Response({"Token": str(token.access_token)})
            return response.Response(
                {"Error": "Invalid access code."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
