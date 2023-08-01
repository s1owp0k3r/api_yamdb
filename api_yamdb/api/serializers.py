from django.shortcuts import get_object_or_404
from django.utils import timezone
from re import fullmatch
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api_yamdb.settings import SLUG_FIELD_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title


class SlugValidationSerializer(serializers.ModelSerializer):
    def validate_slug(self, data):
        """Slug field validation"""
        if (not fullmatch(r"^[-a-zA-Z0-9_]+$", data)
                or len(data) > SLUG_FIELD_LENGTH):
            raise serializers.ValidationError(
                "Slug validation error."
                "Slug either contains invalid chars "
                "or it's length exceeds 50 symbols."
            )
        return data


class CategorySerializer(SlugValidationSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(SlugValidationSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


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

    class Meta(TitleSerializer.Meta):
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
        if (
            Review.objects.filter(
                title=title, author=self.context['request'].user
            ).exists()
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
