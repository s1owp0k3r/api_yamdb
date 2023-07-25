from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ("name", "slug", )


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ("name", "slug", )


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

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


class TitleCRUDSerializer(serializers.ModelSerializer):
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
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
