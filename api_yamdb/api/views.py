from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import SAFE_METHODS
from django.db.models import Avg

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleReadSerializer,
                          TitleCRUDSerializer)


class CreateListDeleteViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin):
    """Generic class for list, create, delete actions"""

    filter_backends = (
        SearchFilter,
    )
    search_fields = ("name",)
    lookup_field = "slug"


class CategoryViewSet(CreateListDeleteViewSet):
    """Categories viewset"""
    # add permissions
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class GenreViewSet(CreateListDeleteViewSet):
    """Genre viewset"""
    # add permissions
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset"""
    # add permissions
    # uncomment once reviews model is available
    # queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (
        SearchFilter,
    )
    search_fields = ("category__slug", "genre__slug", "name", "year", )

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return TitleReadSerializer
        return TitleCRUDSerializer
