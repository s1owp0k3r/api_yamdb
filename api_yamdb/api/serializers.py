from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Title, Comment, Review


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
        """Проверка количества отзывов на произведение у пользователя."""
        title = get_object_or_404(Title, id=self.context['title_id'])
        # добавить в filter условие author=self.context['request'].user
        # после реализации модели юзера
        if (
            Review.objects.filter(title=title).exists()
            and self.context['request'].method == 'POST'
        ):
            raise serializers.ValidationError(
                'Нельзя оставить несколько отзывов на одно произведение!')
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