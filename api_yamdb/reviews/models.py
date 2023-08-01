from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()  # Getting current user model


class Category(models.Model):
    """Categories model"""

    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Genres model"""
    name = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Titles model"""

    name = models.CharField(
        max_length=255
    )
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre,
        through="TitleGenre",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name="titles"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="name_year_unique_relationships",
                fields=["name", "year"]
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.year})"


class TitleGenre(models.Model):
    """Genre to Title relation"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="title"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.DO_NOTHING,
        related_name="genre"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="title_genre_unique_relationships",
                fields=["title", "genre"]
            ),
        ]


class Review(models.Model):
    """Review model"""
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Publication date', auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(models.Model):
    """Comment to review model"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Publication date', auto_now_add=True
    )
