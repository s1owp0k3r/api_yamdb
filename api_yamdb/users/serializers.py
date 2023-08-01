from re import fullmatch
from rest_framework import serializers

from users.models import User

def check_username(username, regex):
    if not fullmatch(regex, username):
        raise serializers.ValidationError('Username does not meet the requirements.')


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

    def validate_username(self, value):
        check_username(value, r'^[\w.@+-]+$')
        if value == 'me':
            raise serializers.ValidationError("Using 'me' as username is not allowed.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """Generic serializer for user."""
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )

    def validate_username(self, value):
        check_username(value, r'^[\w.@+-]+$')
        return value
