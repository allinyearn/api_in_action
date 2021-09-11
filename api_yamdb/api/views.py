from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from .serializers import (
  CommentSerializer, ReviewSerializer, CategorySerializer, GenreSerializer, TitleSerializer
)
from .permissions import AuthorOrReadOnly
from reviews.models import Comment, Review, Title, Category, Genre, Title
from django_filters.rest_framework import DjangoFilterBackend


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для отзывов к произведению.

    Возваращает список всех отзывов, отзыв по id, 
    может добавить обновить и удалить отзыв по id
    """
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Получаем набор отзывов относящихся к определенному произведению"""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.rewiews.all()
        return queryset

    def perform_create(self, serializer):
        """При создании нового отзыва, автор = пользователь создающий отзыв"""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для комментов к отзыву.

    Возваращает список всех комментов к отзыву, коммент по id, 
    может добавить, обновить и удалить коммент по id
    """
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        """Получаем набор комментов относящихся к определенному отзыву"""
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        """При создании нового коммента,
        автор = пользователь создающий коммент,
        отзыв = отзыв с необходимым id
        """
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=name', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category', 'genre', 'name', 'year')
