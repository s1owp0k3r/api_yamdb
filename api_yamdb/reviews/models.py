from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=200)


class Review(models.Model):
    """Review model."""
    text = models.TextField()
    # Раскомментировать после реализации модели пользователя:
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        default=1
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    """Comment to review model."""
    # Раскомментировать после реализации модели пользователя:
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        default=1
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )
