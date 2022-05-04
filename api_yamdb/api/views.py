from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Review, Title

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)


class GetPostDeleteViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        return reviews


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        ...


class CategoryViewSet(GetPostDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = 
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filterset_fields = ('name')
    search_fields = ('name',)
    

class GenreViewSet(GetPostDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = 
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filterset_fields = ('name')
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    # permission_classes = 
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    #filter_backends = (DjangoFilterBackend)
    #filterset_fields=('genre__slug', 'category__slug', 'name', 'year', )

    #def get_queryset(self):
    #    queryset = Title.objects.all()
    #    slug = self.request.query_params.get('slug')
    #    if slug is not None:
    #        queryset = queryset.filter(slug=slug)
    #    return queryset
