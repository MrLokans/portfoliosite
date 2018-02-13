from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from .serializers import (
    PostCreateSerializer,
    PostListSerializer,
)
from .permissions import IsAdminOrReadOnly
from ..models import Post


class PostListAPIView(generics.ListCreateAPIView):
    filter_backends = [SearchFilter, OrderingFilter]
    permission_classes = (IsAdminOrReadOnly, )
    ordering = 'title'
    search_fields = ['title', ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        elif self.request.method == 'POST':
            return PostCreateSerializer
        else:
            raise ValueError("Unknown request method: {}"
                             .format(self.request.method))

    def get_queryset(self):
        qs = Post.objects.all()
        return qs

    def create(self, request, *args, **kwargs):
        """
        Create blog post
        """
        return super().create(request, *args, **kwargs)


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
