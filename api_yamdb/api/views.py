from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title, Review
from .serializers import ReviewSerializer, CommentSerializer

# Убрать эти строчки, когда будут реализована аутентификация:
from django.contrib.auth import get_user_model
User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [] # нужно добавить пермишн

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        return review_title.reviews.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs.get('title_id')
        return context

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        # изменить на author=self.request.user, когда будут реализована аутентификация:
        serializer.save(title=review_title, author=User.objects.get(id=1))


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = [] # нужно добавить пермишн

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        comment_review = get_object_or_404(Review, id=review_id, title_id=title_id)
        return comment_review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        comment_review = get_object_or_404(Review, id=review_id, title_id=title_id)
        # изменить на author=self.request.user, когда будут реализована аутентификация:
        serializer.save(review=comment_review, author=User.objects.get(id=1))
