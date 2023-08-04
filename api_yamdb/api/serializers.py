from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.utils import timezone

from api_yamdb.settings import SLUG_FIELD_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=SLUG_FIELD_LENGTH,
        validators=[UniqueValidator(queryset=Category.objects.all())],
    )

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=SLUG_FIELD_LENGTH,
        validators=[UniqueValidator(queryset=Genre.objects.all())],
    )

    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


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
        slug_field="slug", queryset=Genre.objects.all(), many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "title", "score", "pub_date")
        read_only_fields = ("title",)

    def validate(self, data):
        """Reviews of current user count checking."""
        if (
            Review.objects.filter(
                title=self.context["title_id"],
                author=self.context["request"].user,
            ).exists()
            and self.context["request"].method == "POST"
        ):
            raise serializers.ValidationError(
                "You have already post a review for this title!"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
