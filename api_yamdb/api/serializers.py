import re

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Category, Genre, Title, Comment, Review
)
from api_yamdb.settings import SLUG_FIELD_LENGTH


class CategorySerializer(serializers.ModelSerializer):

    def validate_slug(self, value):
        if (not re.fullmatch(r"^[-a-zA-Z0-9_]+$", value)
                or len(value) > SLUG_FIELD_LENGTH):
            raise serializers.ValidationError(
                "Slug validation error."
                "Slug either contains invalid chars "
                "or it's length exceeds 50 symbols."
            )
        return value

    class Meta:
        model = Category
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"


class TitleSerializer(serializers.ModelSerializer):
    """Generic serializer for Title"""
    rating = serializers.IntegerField(read_only=True, required=False)

    def validate_year(self, value):
        """Validate if year is higher than the current year"""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                "Year validation error."
                f"Specified '{value}' year must be "
                f"less or equal current '{current_year}' year.",
            )
        return value

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitleReadSerializer(TitleSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)


class TitleCRUDSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=["name", "year"]
            )
        ]


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),
        write_only=True,
        default=0
    )


    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        read_only_fields = ('id', 'pub_date')

    def validate(self, data):
        """Reviews of current user count checking."""
        title = get_object_or_404(Title, id=self.context['title_id'])
        # добавить в filter условие author=self.context['request'].user
        # после реализации модели юзера
        if (
            Review.objects.filter(title=title).exists()
            and self.context['request'].method == 'POST'
        ):
            raise serializers.ValidationError(
                'You have already post a review for this title!')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'pub_date')
