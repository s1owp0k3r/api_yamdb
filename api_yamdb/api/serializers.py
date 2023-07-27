from rest_framework import serializers
from django.utils import timezone

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

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

    def validate(self, data):
        """Validate if Title already exists"""

        if not self.context.get("request") == "POST":
            return data

        title_name = self.context.get("view").kwargs.get("name")
        title_year = self.context.get("view").kwargs.get("year")

        if Title.objects.filter(name=title_name, year=title_year).exists():
            raise serializers.ValidationError(
                f"Title with name of '{title_name}' and year '{title_year}'"
                " already exists."
            )
        return data

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
