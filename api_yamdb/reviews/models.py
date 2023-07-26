from django.db import models


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
        related_name="category"
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
