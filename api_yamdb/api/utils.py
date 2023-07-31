import re

from rest_framework import serializers

from api_yamdb.settings import SLUG_FIELD_LENGTH


def validate_slug(data):
    if (not re.fullmatch(r"^[-a-zA-Z0-9_]+$", data)
            or len(data) > SLUG_FIELD_LENGTH):
        raise serializers.ValidationError(
            "Slug validation error."
            "Slug either contains invalid chars "
            "or it's length exceeds 50 symbols."
        )
    return data
