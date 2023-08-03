from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import SLUG_FIELD_LENGTH

User = get_user_model()  # Getting current user model


class CategoryGenreModel(models.Model):
    name = models.CharField(max_length=256, verbose_name="Name")
    slug = models.SlugField(
        unique=True, max_length=SLUG_FIELD_LENGTH, verbose_name="Slug"
    )

    class Meta:
        abstract = True
        ordering = ("id",)

    def __str__(self):
        return self.name


class Category(CategoryGenreModel):
    """Categories model"""

    class Meta(CategoryGenreModel.Meta):
        verbose_name = "category"
        verbose_name_plural = "Categoies"


class Genre(CategoryGenreModel):
    """Genres model"""

    class Meta(CategoryGenreModel.Meta):
        verbose_name = "genre"
        verbose_name_plural = "Genres"


class Title(models.Model):
    """Titles model"""

    name = models.CharField(max_length=256, verbose_name="Name")
    year = models.SmallIntegerField(verbose_name="Year", db_index=True)
    description = models.TextField(verbose_name="Description")
    genre = models.ManyToManyField(
        Genre, through="TitleGenre", verbose_name="Genre"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name="Category",
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "title"
        verbose_name_plural = "Titles"

    def __str__(self):
        return f"{self.name} ({self.year})"


class TitleGenre(models.Model):
    """Genre to Title relation"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="titles",
        verbose_name="Title",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name="genres",
        verbose_name="Genre",
    )


class Review(models.Model):
    """Review model"""

    text = models.TextField(verbose_name="Text")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Author",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Title",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Score",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        verbose_name="Publication date", auto_now_add=True
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "review"
        verbose_name_plural = "Reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_author_title"
            )
        ]

    def __str__(self):
        return f"{self.author} for {self.title}"


class Comment(models.Model):
    """Comment to review model"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Author",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Review",
    )
    text = models.TextField(verbose_name="Text")
    pub_date = models.DateTimeField(
        verbose_name="Publication date", auto_now_add=True
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "comment"
        verbose_name_plural = "Comments"
