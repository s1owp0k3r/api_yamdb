from rest_framework import serializers

from users.models import User


class TokenSerializer(serializers.ModelSerializer):
    """Generic serializer for token."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username", "confirmation_code"
        )


class SignUpSerializer(serializers.ModelSerializer):
    """Generic serializer for registration."""
    class Meta:
        model = User
        fields = (
            "username", "email",
        )


class UserSerializer(serializers.ModelSerializer):
    """Generic serializer for user."""
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )
