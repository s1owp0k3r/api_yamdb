from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters import CharFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from reviews.models import Category, Genre, Review, Title
from .permissions import IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCRUDSerializer, TitleReadSerializer)


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
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('id')


class GenreViewSet(CreateListDeleteViewSet):
    """Genre viewset"""
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by('id')


class TitleFilter(FilterSet):
    """Filter for Title viewset"""
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset"""
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleReadSerializer
        return TitleCRUDSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        return review_title

    def get_queryset(self):
        return self.get_title().reviews.all().order_by('id')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs.get('title_id')
        return context

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Comment viewset"""
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        comment_review = get_object_or_404(
            Review, id=review_id, title_id=title_id
        )
        return comment_review

    def get_queryset(self):
        return self.get_review().comments.all().order_by('id')

    def perform_create(self, serializer):
        serializer.save(review=self.get_review(), author=self.request.user)
