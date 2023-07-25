from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from django.db.models import Avg

from reviews.models import Category, Genre, Title

class CreateListDeleteViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              mixins.DestroyModelMixin):
    pass


class CategoryViewSet(CreateListDeleteViewSet):
    """Categories viewset"""
    # add permissions
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (
        SearchFilter,
    )
    search_fields = ("name", )
    lookup_field = "slug"


class GenreViewSet(CreateListDeleteViewSet):
    """Genre viewset"""
    # add permissions
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (
        SearchFilter,
    )
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset"""
    # add permissions
    serializer_class = TitleSerializer
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = (
        SearchFilter,
    )
    search_fields = ("category__slug", "genre__slug", "name", "year", )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TitleCRUDSerializer
        elif self.action == "destroy":
            return HttpResponse("", status=204)
        return TitleSerializer

