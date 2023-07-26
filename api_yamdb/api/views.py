from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title, Review
from .serializers import ReviewSerializer, ReviewCRUDSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    permission_classes = [] # нужно добавить пермишн

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        return review_title.reviews.all()

    def perform_create(self, serializer):
        """Запись в поле 'title' указанного произведения при сохранении."""
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        serializer.save(title=review_title) # добавить author=self.request.user, когда будут реализована аутентификация

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return ReviewCRUDSerializer
        return ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [] # нужно добавить пермишн

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        comment_review = get_object_or_404(Review, id=review_id, title_id=title_id)
        return comment_review.comments.all()

    def perform_create(self, serializer):
        """Запись в поле 'review' указанного отзыва при сохранении."""
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        comment_review = get_object_or_404(Review, id=review_id, title_id=title_id)
        serializer.save(review=comment_review) # добавить author=self.request.user, когда будут реализована аутентификация
