from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)

from blog.api.serializers import PostListSerializer
from blog.api.permissions import IsAdminOrReadOnly
from blog.models import Post


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = (AllowAny, )
    ordering = 'title'
    # TODO: search by book's notes content
    search_fields = ['title', ]
    # pagination_class = BookPageNumberPagination

    def get_queryset(self):
        qs = Post.objects.all()
        return qs


class PostDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = PostListSerializer

    def destroy(self, request, *args, **kwargs):
        """
        API endpoint for post removal.
        Allowed only for staff users
        """
        return super().destroy(request, *args, **kwargs)

