from re import fullmatch

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UsernameValidationSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        """ "Username validation"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "User with the same username already exists."
            )
        if not fullmatch(r"^[\w.@+-]+$", value):
            raise serializers.ValidationError(
                "Username does not meet the requirements."
            )
        if value == "me":
            raise serializers.ValidationError(
                "Using 'me' as username is not allowed."
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    """Token getting serializer"""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class SignUpSerializer(UsernameValidationSerializer):
    """Serializer for registration."""

    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class UserSerializer(UsernameValidationSerializer):
    """Serializer for user model"""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class ProfileSerializer(UsernameValidationSerializer):
    """Serializer for user profile"""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
