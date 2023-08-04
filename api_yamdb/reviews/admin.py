from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    ordering = ("pk",)
    search_fields = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    ordering = ("pk",)
    search_fields = ("name",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "year",
        "category",
    )
    list_display_links = ("category",)
    ordering = ("pk",)
    search_fields = (
        "name",
        "year",
    )


@admin.register(TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "genre",
    )
    ordering = ("pk",)
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "author", "title", "score", "pub_date")
    ordering = ("pk",)
    search_fields = (
        "author",
        "title",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "author", "review", "pub_date")
    ordering = ("pk",)
    search_fields = (
        "author",
        "review",
    )
