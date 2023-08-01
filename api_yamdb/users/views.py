from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from django.core.mail.message import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import response, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .permissions import IsAdmin
from .serializers import (
    ProfileSerializer,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer
)

NOT_PUT_REQUESTS = [
    'get', 'post', 'patch', 'delete'
]


class UserViewSet(viewsets.ModelViewSet):
    """User viewset."""
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    http_method_names = NOT_PUT_REQUESTS
    lookup_field = "username"
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def profile(self, request):
        if request.method == "PATCH":
            serializer = ProfileSerializer(
                self.request.user,
                data=request.data,
                partial=True
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
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
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
