from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from django.db.models import Avg

from .permissions import IsAdminOrReadOnly, IsAdminModeratorAuthorOrReadOnly
from reviews.models import Category, Genre, Title, Review
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleCRUDSerializer,
    ReviewSerializer,
    CommentSerializer
)


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
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset"""
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score')).order_by('id')
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

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        return review_title.reviews.all().order_by('id')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs.get('title_id')
        return context

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        serializer.save(title=review_title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Comment viewset"""
    serializer_class = CommentSerializer
    ppermission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        comment_review = get_object_or_404(Review, id=review_id, title_id=title_id)
        return comment_review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        comment_review = get_object_or_404(Review, id=review_id, title_id=title_id)
        serializer.save(review=comment_review, author=self.request.user)
