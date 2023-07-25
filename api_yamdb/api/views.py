from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Title
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [] # нужно написать кастомный пермишн - Денис

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        return review_title.reviews.all()

    def perform_create(self, serializer):
        """Запись в поле 'title' указанного произведения при сохранении."""
        title_id = self.kwargs.get('title_id')
        review_title = get_object_or_404(Title, id=title_id)
        serializer.save(title=review_title) # добавить author=self.request.user, когда будут реализована аутентификация