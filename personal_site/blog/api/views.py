from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from blog.models import Post
from blog.api.serializers import PostListSerializer


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = 'title'
    # TODO: search by book's notes content
    search_fields = ['title', ]
    # pagination_class = BookPageNumberPagination

    def get_queryset(self):
        qs = Post.objects.all()
        return qs
