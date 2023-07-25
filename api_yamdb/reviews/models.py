from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=200)


class Review(models.Model):
    text = models.TextField()
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='reviews'
    # )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )