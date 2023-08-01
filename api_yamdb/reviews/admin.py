from django.contrib import admin

from .models import Category, Genre, Title, TitleGenre


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",)
    ordering = ("pk",)
    search_fields = ("name", )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", )
    ordering = ("pk", )
    search_fields = ("name",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "category", )
    list_display_links = ("category", )
    ordering = ("pk",)
    search_fields = ("name", "year", )


@admin.register(TitleGenre)
class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "genre", )
    ordering = ("pk",)
    search_fields = ("title", )
